import streamlit as st
import pandas as pd
# data.py 파일로부터 데이터베이스 구조 분리 호출
from data import curriculum_db, major_db

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="고교학점제 과목 선택 지원 시스템", layout="wide")

st.title("🏫 울산가온고 맞춤형 고교학점제 과목 설계 시스템")
st.write("2026학년도 교육과정 편성표 규정이 적용된 프로그램입니다.")

major_options = []
for cat in major_db.keys():
    for maj in major_db[cat].keys():
        major_options.append(f"{cat} ➡️ {maj}")

all_unique_subjects = set()
for grade in curriculum_db.values():
    for semester in grade.values():
        for group in semester.values():
            all_unique_subjects.update(group["과목"])

def get_subject_explanation(sub_name, major_name):
    reason = f"{major_name} 전공 이수에 필요한 기초 학업 성취도와 논리적 사고력을 기르는 과목입니다."
    benefit = "학생부 종합 전형 정성 평가에서 성실성과 학업 전반의 기초 체력을 입증할 수 있습니다."
    
    if "미적분" in sub_name:
        reason = f"{major_name} 전공의 고등 학술 연구에 핵심이 되는 수학적 모델링 능력 및 다차원 해석 기법을 체득합니다."
        benefit = "대학 진학 후 전공 수학 및 메커니즘 해석 수업의 학업 공백을 예방하고 신뢰도를 대폭 높입니다."
    elif "데이터 과학" in sub_name or "소프트웨어" in sub_name:
        reason = f"4차 산업 핵심 기술인 알고리즘 설계 역량과 대용량 데이터 정제 체계를 실습하는 필수 전공 연계 교과입니다."
        benefit = "첨단 융합형 공학 인재로서의 실무 프로그래밍 잠재력을 입증하여 학생부 경쟁력을 선점합니다."
    elif "물리학" in sub_name or "역학" in sub_name or "전자기" in sub_name:
        reason = f"{major_name} 인프라의 핵심인 하드웨어 메커니즘과 자연물리 법칙을 공학적으로 구현하는 기초 학문입니다."
        benefit = "이공계 전공 평가진이 가장 중요하게 검토하는 하드웨어 및 시스템 구현 역량을 시각화합니다."
    elif "화학" in sub_name or "물질" in sub_name:
        reason = f"미세 물질의 분자 반응과 신소재 메커니즘을 규명하여 전공 관련 실험 설계의 뼈대를 다집니다."
        benefit = "소재 및 바이오, 화학공학 분야의 정밀 전공 적합성을 충실하게 표현할 수 있습니다."
    elif "생명과학" in sub_name or "세포" in sub_name or "유전" in sub_name:
        reason = f"생명체의 본질적 생리 대사와 유전 정보를 심층 분석하여 바이오·보건 학문적 베이스를 구축합니다."
        benefit = "의예, 약학, 간호 계열 학생부 평가에서 학종 합격을 결정짓는 결정적 정성 평가요소입니다."
    elif "확률과 통계" in sub_name or "실용 통계" in sub_name:
        reason = f"연구 가설의 타당성을 검증하고, 현장 데이터를 과학적으로 분석해 내는 정량적 추론 도구입니다."
        benefit = "계열을 불문하고 객관적인 통계 분석 및 데이터 기반 의사결정 능력을 갖추었음을 강조합니다."
    elif "경제" in sub_name:
        reason = f"시장 원리와 합리적 경제 모형을 학습하여 전공 분야에 결합할 실무 경제적 시각을 확장합니다."
        benefit = "상경 및 사회과학 계열 진학 시 융합적 학업 태도를 돋보이게 하는 요소로 작용합니다."
        
    return reason, benefit

def calculate_dynamic_scores(major_name, category_name, passed_list, current_grade_mode):
    rules = major_db[category_name][major_name]
    scores = {}
    for sub in all_unique_subjects:
        if sub in rules.get("핵심", []):
            relation_score = 70
        elif sub in rules.get("권장", []):
            relation_score = 50
        else:
            relation_score = 30
            
        if current_grade_mode == "1학년":
            connection_score = 30
        else:
            if sub in ["미적분II", "기하", "경제 수학", "수학과제 탐구", "실용 통계"]:
                connection_score = 30 if "확률과 통계" in passed_list else 10
            elif sub in ["전자기와 양자", "역학과 에너지"]:
                connection_score = 30 if "물리학" in passed_list else 10
            elif sub in ["화학 반응의 세계", "물질과 에너지"]:
                connection_score = 30 if "화학" in passed_list else 10
            elif sub in ["생물의 유전", "세포와 물질대사"]:
                connection_score = 30 if "생명과학" in passed_list else 10
            elif sub in ["행성우주과학", "지구시스템과학"]:
                connection_score = 30 if "지구과학" in passed_list else 10
            else:
                connection_score = 30
                
        scores[sub] = relation_score + connection_score
    return scores

# [수정 사항]: 완전 리팩토링된 정밀 AI 진단 알고리즘 함수
def run_ai_diagnosis(selected_list, major_name, category_name, grade_label):
    if category_name not in major_db or major_name not in major_db[category_name]:
        return
    rules = major_db[category_name][major_name]
    
    st.write("---")
    st.subheader(f"🔬 울산가온고 전공 적합성 AI 정밀 진단 리포트 ({grade_label})")
    
    # 각 검사 대상 학년에 실제로 개설된 과목 풀 파싱
    if "2학년" in grade_label:
        grade_subjects = (curriculum_db["2학년"]["1학기"]["영사과_택3"]["과목"] + 
                          curriculum_db["2학년"]["1학기"]["외국어_택1"]["과목"] + 
                          curriculum_db["2학년"]["2학기"]["주요_택3"]["과목"] + 
                          curriculum_db["2학년"]["2학기"]["외국어_택1"]["과목"])
    else:
        grade_subjects = (curriculum_db["3학년"]["1학기"]["주요_택5"]["과목"] + 
                          curriculum_db["3학년"]["1학기"]["지정_택1"]["과목"] + 
                          curriculum_db["3학년"]["1학기"]["예술_택1"]["과목"] + 
                          curriculum_db["3학년"]["2학기"]["주요_택5"]["과목"] + 
                          curriculum_db["3학년"]["2학기"]["지정_택1"]["과목"] + 
                          curriculum_db["3학년"]["2학기"]["예술_택1"]["과목"])
                          
    # 전체 마스터 데이터 중 본 학년에 개설되는 전공 핵심/권장 과목만 분모로 동적 재정의
    total_target_cores = [sub for sub in rules.get("핵심", []) if sub in grade_subjects]
    total_target_recoms = [sub for sub in rules.get("권장", []) if sub in grade_subjects]
    
    core_in_selected = [sub for sub in total_target_cores if sub in selected_list]
    recom_in_selected = [sub for sub in total_target_recoms if sub in selected_list]
    
    missing_cores = [sub for sub in total_target_cores if sub not in selected_list]
    missing_recoms = [sub for sub in total_target_recoms if sub not in selected_list]
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("현재 설계된 이수 과목 수", f"{len(selected_list)}개")
    with col_stat2:
        st.metric("본 학년 핵심 과목 충족도", f"{len(core_in_selected)}개 / {len(total_target_cores)}개")
    with col_stat3:
        st.metric("본 학년 권장 과목 매칭", f"{len(recom_in_selected)}개 / {len(total_target_recoms)}개")
        
    # 예외 상황 처리 분기 (2학년에 핵심과목이 아예 개설되지 않는 학과 대비)
    if len(total_target_cores) == 0:
        st.info(f"ℹ️ **[학년별 교육과정 편성 안내]**\n\n울산가온고 교육과정 구조상 **2학년** 시기에는 **{major_name}**의 필수 핵심 교과목(데이터 과학 등)이 편성되어 있지 않으며, 해당 심화 과목들은 전부 **3학년**에 배치되어 있습니다. 따라서 2학년 충족도가 0개로 표시되는 것은 정상입니다. 이 시기에는 학과의 학술적 기초를 다지는 권장 교과(확률과 통계, 물리학 등)를 규정에 맞게 밀도 있게 이수했는지가 정성 평가의 절대적 척도가 됩니다.")
        if len(missing_recoms) == 0 and len(recom_in_selected) > 0:
            st.success(f"✅ **[{grade_label} 최적화 완료]** 현재 2학년 과정에서 선택 가능한 학과 필수 권장 과목({', '.join(recom_in_selected)})을 교육과정 규칙에 맞춰 완벽히 선택하셨습니다. 학년 진도 대비 우수한 학업 전공 설계안입니다.")
        elif len(missing_recoms) > 0:
            st.warning(f"⚠️ **[기초 권장 과목 보완 권고]** 현재 2학년 개설 과목 중 해당 전공의 3학년 심화 수업 연계에 발판이 되는 권장 교과인 **[{', '.join(missing_recoms)}]** 과목이 설계안에서 누락되어 있습니다. 이수 조정을 권장합니다.")
    else:
        if len(missing_cores) == 0:
            st.success(f"🎯 **[{grade_label} 우수 설계 조합 확인]**\n\n현재 제출하신 **{grade_label}**은 **{major_name}** 합격을 위해 본 학년에 배치된 핵심 전공 연계 교과목을 누락 없이 충족합니다. 고교학점제의 취지에 완벽히 부합하며, 대학 학생부 종합 전형 정성 평가 시 학업 역량 부문에서 경쟁력을 확보할 수 있는 견고한 선택안입니다.")
        else:
            st.warning(f"⚠️ **[{grade_label} 전공 연계성 보완 필요]**\n\n현재 제출하신 **{grade_label}**은 **{major_name}** 진학 시 대학 사정관들이 필수 이수를 요구하는 핵심 과목 중 일부가 누락되어 정성 평가 상의 리스크가 존재합니다.")
            st.markdown(f"🚨 **본 학년 미이수 핵심 과목**: {', '.join([f'**{m}**' for m in missing_cores])}")
            st.markdown(f"📖 **입학사정관 정성 평가 피드백**: 해당 학년에 이수할 수 있는 핵심 과목을 기피하고 평이한 교양 과목 위주로 채울 경우 전공 탐구 역량에서 감점 요인이 될 수 있습니다. 학과 연관성이 낮은 일반 선택 과목 대신 필수 연계 교과인 **[{', '.join(missing_cores)}]** 과목으로 교체 조율하십시오.")

# 학년 선택용 라디오 버튼
st.subheader("🎯 본인의 현재 학년을 선택해 주세요")
grade_auth = st.radio(
    "학년 선택에 따라 이수 과목 설계 범위 및 70:30 적합도 산출 가중치가 동적으로 변환됩니다.", 
    ["현재 1학년 (2학년 선택과목 설계 시기)", "현재 2학년 (3학년 선택과목 설계 시기)"],
    key="main_grade_timeline"
)

passed_subjects = []

# ------------------------------------------
# CASE A: 현재 1학년 프로세스
# ------------------------------------------
if grade_auth == "현재 1학년 (2학년 선택과목 설계 시기)":
    tab1, tab2, tab3 = st.tabs(["📘 2·3학년 교육과정 설계", "🤖 2·3학년 통합 최적 패키지 추천", "💡 시스템 가이드"])
    
    with tab1:
        st.header("📋 2·3학년 연속 수강 신청 시뮬레이션")
        selected_option_t1 = st.selectbox("🎯 목표 계열 및 학과를 선택하세요:", major_options, key="t1_major_select_1")
        t1_cat, t1_maj = selected_option_t1.split(" ➡️ ")
        
        st.write("---")
        st.subheader("🌱 [STEP 1] 2학년 개설 선택과목 시뮬레이션")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**[1학기] 영/사/과 중 택 3 (각 4학점)**")
            g1_selected = []
            for sub in curriculum_db["2학년"]["1학기"]["영사과_택3"]["과목"]:
                if st.checkbox(sub, key=f"2_1_g1_1_{sub}"): g1_selected.append(sub)
            st.caption(f"선택 현황: {len(g1_selected)} / 3 개")
        with col2:
            st.write("**[1학기] 제2외국어 중 택 1 (각 3학점)**")
            g2_selected = []
            for sub in curriculum_db["2학년"]["1학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"2_1_g2_1_{sub}"): g2_selected.append(sub)
            st.caption(f"선택 현황: {len(g2_selected)} / 1 개")
            
        col3, col4 = st.columns(2)
        with col3:
            st.write("**[2학기] 국/수/영/사/과 중 택 3 (각 4학점)**")
            g3_selected = []
            for sub in curriculum_db["2학년"]["2학기"]["주요_택3"]["과목"]:
                if st.checkbox(sub, key=f"2_2_g3_1_{sub}"): g3_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_selected)} / 3 개")
        with col4:
            st.write("**[2학기] 제2외국어 중 택 1 (각 3학점)**")
            g4_selected = []
            for sub in curriculum_db["2학년"]["2학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"2_2_g4_1_{sub}"): g4_selected.append(sub)
            st.caption(f"선택 현황: {len(g4_selected)} / 1 개")

        if st.button("🚀 2학년 선택안 AI 진단 결과 보기", key="btn_t1_diag_1"):
            if len(g1_selected) != 3 or len(g2_selected) != 1 or len(g3_selected) != 3 or len(g4_selected) != 1:
                st.error("❌ 학교 지정 2학년 학점 선택 규정을 위반했습니다. 조건 개수를 정확히 확인 후 재시도하십시오.")
            else:
                t1_total = g1_selected + g2_selected + g3_selected + g4_selected
                run_ai_diagnosis(t1_total, t1_maj, t1_cat, "2학년 과목 설계안")

        st.write("---")
        st.subheader("🌲 [STEP 2] 3학년 개설 선택과목 시뮬레이션")
        col_3_1_1, col_3_1_2, col_3_1_3 = st.columns(3)
        with col_3_1_1:
            st.write("**[1학기] 국/영/수/사/과 중 택 5 (각 4학점)**")
            g3_1_1_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["주요_택5"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g1_1_{sub}"): g3_1_1_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_1_selected)} / 5 개")
        with col_3_1_2:
            st.write("**[1학기] 제2외국어/교양/기정 택 1 (각 3학점)**")
            g3_1_2_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["지정_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g2_1_{sub}"): g3_1_2_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_2_selected)} / 1 개")
        with col_3_1_3:
            st.write("**[1학기] 예술 중 택 1 (각 3학점)**")
            g3_1_3_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["예술_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g3_1_{sub}"): g3_1_3_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_3_selected)} / 1 개")
            
        col_3_2_1, col_3_2_2, col_3_2_3 = st.columns(3)
        with col_3_2_1:
            st.write("**[2학기] 국/영/수/사/과 중 택 5 (각 4학점)**")
            g3_2_1_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["주요_택5"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g1_1_{sub}"): g3_2_1_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_1_selected)} / 5 개")
        with col_3_2_2:
            st.write("**[2학기] 제2외국어/교양/기정 택 1 (각 3학점)**")
            g3_2_2_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["지정_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g2_1_{sub}"): g3_2_2_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_2_selected)} / 1 개")
        with col_3_2_3:
            st.write("**[2학기] 예술 중 택 1 (각 3학점)**")
            g3_2_3_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["예술_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g3_1_{sub}"): g3_2_3_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_3_selected)} / 1 개")

        if st.button("🚀 3학년 선택안 AI 진단 결과 보기", key="btn_t2_diag_1"):
            if len(g3_1_1_selected) != 5 or len(g3_1_2_selected) != 1 or len(g3_1_3_selected) != 1 or \
               len(g3_2_1_selected) != 5 or len(g3_2_2_selected) != 1 or len(g3_2_3_selected) != 1:
                st.error("❌ 학교 지정 3학년 수강 신청 학점 규정을 준수하지 않았습니다. 조건 개수를 확인하십시오.")
            else:
                t2_total = g3_1_1_selected + g3_1_2_selected + g3_1_3_selected + g3_2_1_selected + g3_2_2_selected + g3_2_3_selected
                run_ai_diagnosis(t2_total, t1_maj, t1_cat, "3학년 과목 설계안")

    with tab2:
        st.header("🤖 2·3학년 통합 최적 패키지 추천")
        selected_option_t3 = st.selectbox("🎯 목표 계열 및 학과를 선택하세요:", major_options, key="t3_major_select_1")
        t3_cat, t3_maj = selected_option_t3.split(" ➡️ ")
        
        if t3_maj:
            scores_dict = calculate_dynamic_scores(t3_maj, t3_cat, [], "1학년")
            final_recommended_records = []
            
            for grade_name, grade_val in curriculum_db.items():
                for sem_name, sem_val in grade_val.items():
                    for group_name, group_val in sem_val.items():
                        group_records = []
                        for sub in group_val["과목"]:
                            r_reason, r_benefit = get_subject_explanation(sub, t3_maj)
                            group_records.append({
                                "학년": grade_name,
                                "학기": sem_name,
                                "그룹명": group_name.split("_")[0],
                                "과목명": sub,
                                "단위수": group_val["학점"],
                                "적합도 점수": scores_dict.get(sub, 60),
                                "추천 이유": r_reason,
                                "이수 장점": r_benefit
                            })
                        df_group = pd.DataFrame(group_records).sort_values(by="적합도 점수", ascending=False)
                        top_n = df_group.head(group_val["선택개수"])
                        final_recommended_records.extend(top_n.to_dict(orient="records"))
            
            df_all = pd.DataFrame(final_recommended_records).sort_values(by="적합도 점수", ascending=False).reset_index(drop=True)
            df_all.insert(0, "순위", list(range(1, len(df_all) + 1)))
            
            st.subheader(f"📋 2·3학년 통합 정밀 추천 포트폴리오 (총 22개 과목 일괄 구성)")
            st.caption("💡 **안내**: '추천 이유'와 '이수 장점'의 구체적인 내용이 잘려 보일 경우, 해당 칸을 **더블클릭**하시면 전체 내용을 자세히 확인하실 수 있습니다.")
            st.dataframe(df_all, use_container_width=True, hide_index=True)

    with tab3:
        st.header("💡 1학년 사용자를 위한 시스템 가이드")
        st.info("현재 1학년 학생은 고교학점제 규정상 2학년과 3학년 과목 설계를 순차적으로 연속 진행해야 합니다. 1번 탭에서 2학년 및 3학년 시뮬레이션을 원스톱으로 마친 뒤, 2번 탭에서 전공에 필요한 22개 매칭 과목 리스트를 받아보십시오.")

# ------------------------------------------
# CASE B: 현재 2학년 프로세스
# ------------------------------------------
else:
    # [수정 사항 5]: 한자어 기이수를 한글 '2학년 때 이수 과목'으로 직관적 변경
    tab1, tab2, tab3 = st.tabs(["🎒 2학년 때 이수 과목", "📗 3학년 교육과정 설계", "🤖 3학년 맞춤 최적 패키지 추천"])
    
    with tab1:
        st.header("🎒 2학년 때 이수했던 과목을 체크해 주세요")
        st.write("3학년 과목의 30% 가중치인 '과목 연계성 점수'를 연산하기 위한 과거 이력 추적 장치입니다.")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.subheader("📌 2학년 1학기 이수 내역 확인")
            st.write("**[그룹 1] 영/사/과 중 택 3 (각 4학점)**")
            passed_2_1_g1 = []
            for sub in curriculum_db["2학년"]["1학기"]["영사과_택3"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_1_g1_{sub}"): passed_2_1_g1.append(sub)
            st.caption(f"선택 현황: {len(passed_2_1_g1)} / 3 개")
            
            st.write("**[그룹 2] 제2외국어 중 택 1 (각 3학점)**")
            passed_2_1_g2 = []
            for sub in curriculum_db["2학년"]["1학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_1_g2_{sub}"): passed_2_1_g2.append(sub)
            st.caption(f"선택 현황: {len(passed_2_1_g2)} / 1 개")
            
        with col_p2:
            st.subheader("📌 2학년 2학기 이수 내역 확인")
            st.write("**[그룹 1] 국/수/영/사/과 중 택 3 (각 4학점)**")
            passed_2_2_g1 = []
            for sub in curriculum_db["2학년"]["2학기"]["주요_택3"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_2_g3_{sub}"): passed_2_2_g1.append(sub)
            st.caption(f"선택 현황: {len(passed_2_2_g1)} / 3 개")
            
            st.write("**[그룹 2] 제2외국어 중 택 1 (각 3학점)**")
            passed_2_2_g2 = []
            for sub in curriculum_db["2학년"]["2학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_2_g4_{sub}"): passed_2_2_g2.append(sub)
            st.caption(f"선택 현황: {len(passed_2_2_g2)} / 1 개")
                
        passed_subjects = passed_2_1_g1 + passed_2_1_g2 + passed_2_2_g1 + passed_2_2_g2
        
        st.write("---")
        st.success(f"현재 시스템이 인지한 2학년 이수 과목 개수: **{len(passed_subjects)}개**")
        st.info("💡 본인의 실제 2학년 학생부 이수 내역과 수치(택3, 택1 등)가 정확히 일치하는지 확인 후, 2번 및 3번 탭으로 이동하여 주십시오.")

    with tab2:
        st.header("📋 3학년 수강 신청 시뮬레이션")
        
        # [수정 사항 4]: 2학년 데이터 실시간 동기화 명시 안내문 추가
        st.info(f"🔄 **실시간 연계 연산 완료**: 1번 탭(2학년 때 이수 과목)에서 선택하신 총 **{len(passed_subjects)}개**의 과목과의 학업적 선후 관계를 추적하여, 3학년 심화 선택 과목 설계 시 30%의 연계 가중치가 자동 대입 중입니다.")
        
        selected_option_t2_3 = st.selectbox("🎯 목표 계열 및 학과를 선택하세요:", major_options, key="t2_3_major_select_2")
        t2_3_cat, t2_3_maj = selected_option_t2_3.split(" ➡️ ")
        
        st.subheader("📌 1학기 선택")
        col_311, col_312, col_313 = st.columns(3)
        with col_311:
            st.write("**[그룹 1] 국/영/수/사/과 중 택 5 (각 4학점)**")
            g3_1_1_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["주요_택5"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g1_2_{sub}"): g3_1_1_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_1_selected)} / 5 개")
        with col_312:
            st.write("**[그룹 2] 제2외국어/교양/기정 택 1 (각 3학점)**")
            g3_1_2_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["지정_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g2_2_{sub}"): g3_1_2_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_2_selected)} / 1 개")
        with col_313:
            st.write("**[그룹 3] 예술 중 택 1 (각 3학점)**")
            g3_1_3_selected = []
            for sub in curriculum_db["3학년"]["1학기"]["예술_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_1_g3_2_{sub}"): g3_1_3_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_1_3_selected)} / 1 개")
            
        st.subheader("📌 2학기 선택")
        col_321, col_322, col_323 = st.columns(3)
        with col_321:
            st.write("**[그룹 1] 국/영/수/사/과 중 택 5 (각 4학점)**")
            g3_2_1_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["주요_택5"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g1_2_{sub}"): g3_2_1_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_1_selected)} / 5 개")
        with col_322:
            st.write("**[그룹 2] 제2외국어/교양/기정 택 1 (각 3학점)**")
            g3_2_2_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["지정_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g2_2_{sub}"): g3_2_2_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_2_selected)} / 1 개")
        with col_323:
            st.write("**[그룹 3] 예술 중 택 1 (각 3학점)**")
            g3_2_3_selected = []
            for sub in curriculum_db["3학년"]["2학기"]["예술_택1"]["과목"]:
                if st.checkbox(sub, key=f"3_2_g3_2_{sub}"): g3_2_3_selected.append(sub)
            st.caption(f"선택 현황: {len(g3_2_3_selected)} / 1 개")

        if st.button("🚀 3학년 설계안 AI 진단받기", key="btn_t2_3_diag_2"):
            if len(g3_1_1_selected) != 5 or len(g3_1_2_selected) != 1 or len(g3_1_3_selected) != 1 or \
               len(g3_2_1_selected) != 5 or len(g3_2_2_selected) != 1 or len(g3_2_3_selected) != 1:
                st.error("❌ 학교 지정 수강 신청 학점 규정을 준수하지 않았습니다. 조건 개수를 확인하십시오.")
            else:
                t2_total = g3_1_1_selected + g3_1_2_selected + g3_1_3_selected + g3_2_1_selected + g3_2_2_selected + g3_2_3_selected
                run_ai_diagnosis(t2_total, t2_3_maj, t2_3_cat, "3학년 과목 설계안")

    with tab3:
        st.header("🤖 3학년 맞춤 최적 패키지 추천")
        st.write("2학년 이수 이력을 바탕으로, 3학년 교육과정 내에서 선택할 수 있는 **총 14개 최적 과목 조합**을 스코어링합니다.")
        selected_option_t3_3 = st.selectbox("🎯 목표 계열 및 학과를 선택하세요:", major_options, key="t3_3_major_select_2")
        t3_3_cat, t3_3_maj = selected_option_t3_3.split(" ➡️ ")
        
        if t3_3_maj:
            scores_dict = calculate_dynamic_scores(t3_3_maj, t3_3_cat, passed_subjects, "2학년")
            final_recommended_records = []
            
            for sem_name, sem_val in curriculum_db["3학년"].items():
                for group_name, group_val in sem_val.items():
                    group_records = []
                    for sub in group_val["과목"]:
                        r_reason, r_benefit = get_subject_explanation(sub, t3_3_maj)
                        group_records.append({
                            "학년": "3학년",
                            "학기": sem_name,
                            "그룹명": group_name.split("_")[0],
                            "과목명": sub,
                            "단위수": group_val["학점"],
                            "적합도 점수": scores_dict.get(sub, 60),
                            "추천 이유": r_reason,
                            "이수 장점": r_benefit
                        })
                    df_group = pd.DataFrame(group_records).sort_values(by="적합도 점수", ascending=False)
                    top_n = df_group.head(group_val["선택개수"])
                    final_recommended_records.extend(top_n.to_dict(orient="records"))
            
            df_all = pd.DataFrame(final_recommended_records).sort_values(by="적합도 점수", ascending=False).reset_index(drop=True)
            df_all.insert(0, "순위", list(range(1, len(df_all) + 1)))
            
            st.subheader(f"📋 3학년 맞춤 최적화 포트폴리오 (총 14개 과목 구성)")
            st.caption("💡 **안내**: '추천 이유'와 '이수 장점'의 구체적인 내용이 잘려 보일 경우, 해당 칸을 **더블클릭**하시면 전체 내용을 자세히 확인하실 수 있습니다.")
            st.dataframe(df_all, use_container_width=True, hide_index=True)