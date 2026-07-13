import streamlit as st
import pandas as pd

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="고교학점제 과목 선택 지원 시스템", layout="wide")

st.title("🏫 우리 학교 맞춤형 고교학점제 과목 설계 시스템")
st.write("2026학년도 입학생 교육과정 편성표 규정 및 70:30 정밀 가중치 적합도 연산 알고리즘이 적용된 프로그램입니다.")

# 2. 학년별/학기별/선택그룹별 상세 데이터베이스 구축
curriculum_db = {
    "2학년": {
        "1학기": {
            "영사과_택3": {"과목": ["영어 발표와 토론", "세계시민과 지리", "사회와 문화", "현대사회와 윤리", "물리학", "화학", "생명과학", "지구과학"], "학점": 4, "선택개수": 3},
            "외국어_택1": {"과목": ["일본어", "중국어"], "학점": 3, "선택개수": 1}
        },
        "2학기": {
            "주요_택3": {"과목": ["주제 탐구 독서", "확률과 통계", "영미 문학 읽기", "세계사", "한국지리 탐구", "정치", "인문학과 윤리", "역학과 에너지", "물질과 에너지", "세포와 물질대사", "지구시스템과학"], "학점": 4, "선택개수": 3},
            "외국어_택1": {"과목": ["일본 문화", "중국 문화"], "학점": 3, "선택개수": 1}
        }
    },
    "3학년": {
        "1학기": {
            "주요_택5": {"과목": ["독서와 작문", "문학과 영상", "영어 독해와 작문", "심화 영어", "미적분II", "기하", "경제 수학", "수학과제 탐구", "도시의 미래 탐구", "윤리와 사상", "역사로 탐구하는 현대 세계", "사회문제 탐구", "전자기와 양자", "화학 반응의 세계", "생물의 유전", "행성우주과학"], "학점": 4, "선택개수": 5},
            "지정_택1": {"과목": ["일본어 회화", "중국어 회화", "생태와 환경", "데이터 과학"], "학점": 3, "선택개수": 1},
            "예술_택1": {"과목": ["음악 연주와 창작", "미술 창작"], "학점": 3, "선택개수": 1}
        },
        "2학기": {
            "주요_택5": {"과목": ["독서 토론과 글쓰기", "매체 의사소통", "언어생활 탐구", "실생활 영어 회화", "미디어 영어", "실용 통계", "법과 사회", "여행지리", "윤리문제 탐구", "과학의 역사와 문화", "융합과학 탐구", "기후변화와 환경생태"], "학점": 4, "선택개수": 5},
            "지정_택1": {"과목": ["심화 일본어", "심화 중국어", "인간과 심리", "소프트웨어와 생활"], "학점": 3, "선택개수": 1},
            "예술_택1": {"과목": ["음악 감상과 비평", "미술 감상과 비평"], "학점": 3, "선택개수": 1}
        }
    }
}

# 63개 학과 마스터 데이터 정의 (의예과 오타 교정 완료)
major_db = {
    "공학계열": {
        "컴퓨터공학과": {"핵심": ["데이터 과학", "소프트웨어와 생활", "미적분II"], "권장": ["확률과 통계", "기하", "실용 통계"]},
        "정보보안학과": {"핵심": ["데이터 과학", "소프트웨어와 생활", "정보"], "권장": ["미적분II", "확률과 통계", "기하"]},
        "소프트웨어학과": {"핵심": ["소프트웨어와 생활", "데이터 과학", "미적분II"], "권장": ["기하", "확률과 통계", "인공지능 수학"]},
        "산업공학과": {"핵심": ["확률과 통계", "데이터 과학", "경제 수학"], "권장": ["미적분II", "실용 통계", "소프트웨어와 생활"]},
        "전자공학과": {"핵심": ["물리학", "전자기와 양자", "미적분II"], "권장": ["기하", "데이터 과학", "소프트웨어와 생활"]},
        "기계공학과": {"핵심": ["물리학", "역학과 에너지", "미적분II"], "권장": ["기하", "수학과제 탐구", "과학의 역사와 문화"]},
        "화학공학과": {"핵심": ["화학", "화학 반응의 세계", "미적분II"], "권장": ["융합과학 탐구", "물질과 에너지", "수학과제 탐구"]},
        "신소재공학과": {"핵심": ["물리학", "화학", "물질과 에너지"], "권장": ["미적분II", "화학 반응의 세계", "전자기와 양자"]},
        "건축학과": {"핵심": ["물리학", "도시의 미래 탐구", "기하"], "권장": ["미적분II", "세계시민과 지리", "여행지리"]},
        "환경공학과": {"핵심": ["화학", "생태와 환경", "기후변화와 환경생태"], "권장": ["생명과학", "융합과학 탐구", "사회문제 탐구"]},
        "항공우주공학과": {"핵심": ["물리학", "역학과 에너지", "행성우주과학"], "권장": ["미적분II", "기하", "전자기와 양자"]},
        "토목공학과": {"핵심": ["물리학", "역학과 에너지", "지구과학"], "권장": ["미적분II", "기하", "도시의 미래 탐구"]},
        "바이오메디컬공학과": {"핵심": ["생명과학", "세포와 물질대사", "데이터 과학"], "권장": ["미적분II", "화학", "소프트웨어와 생활"]},
        "인공지능학과": {"핵심": ["인공지능 수학", "데이터 과학", "소프트웨어와 생활"], "권장": ["미적분II", "확률과 통계", "실용 통계"]},
        "데이터사이언스학과": {"핵심": ["데이터 과학", "확률과 통계", "실용 통계"], "권장": ["인공지능 수학", "소프트웨어와 생활", "미적분II"]}
    },
    "자연과학계열": {
        "수학과": {"핵심": ["미적분II", "확률과 통계", "기하"], "권장": ["수학과제 탐구", "인공지능 수학", "실용 통계"]},
        "통계학과": {"핵심": ["확률과 통계", "실용 통계", "데이터 과학"], "권장": ["경제 수학", "인공지능 수학", "미적분II"]},
        "물리학과": {"핵심": ["물리학", "역학과 에너지", "전자기와 양자"], "권장": ["미적분II", "기하", "과학의 역사와 문화"]},
        "화학과": {"핵심": ["화학", "물질과 에너지", "화학 반응의 세계"], "권장": ["미적분II", "융합과학 탐구", "과학의 역사와 문화"]},
        "생명과학과": {"핵심": ["생명과학", "세포와 물질대사", "생물의 유전"], "권장": ["화학", "융합과학 탐구", "기후변화와 환경생태"]},
        "지구환경과학과": {"핵심": ["지구과학", "지구시스템과학", "기후변화와 환경생태"], "권장": ["화학", "행성우주과학", "생태와 환경"]},
        "천문우주학과": {"핵심": ["지구과학", "지구시스템과학", "행성우주과학"], "권장": ["물리학", "역학과 에너지", "미적분II"]},
        "식품영양학과": {"핵심": ["화학", "생명과학", "세포와 물질대사"], "권장": ["융합과학 탐구", "확률과 통계"]},
        "해양학과": {"핵심": ["지구과학", "지구시스템과학", "기후변화와 환경생태"], "권장": ["생태와 환경", "융합과학 탐구"]},
        "분자생물학과": {"핵심": ["생명과학", "세포와 물질대사", "생물의 유전"], "권장": ["화학", "화학 반응의 세계"]}
    },
    "인문사회계열": {
        "경영학과": {"핵심": ["경제 수학", "확률과 통계", "사회문제 탐구"], "권장": ["데이터 과학", "실용 통계", "법과 사회"]},
        "경제학과": {"핵심": ["경제 수학", "확률과 통계", "미적분II"], "권장": ["실용 통계", "데이터 과학", "사회문제 탐구"]},
        "정치외교학과": {"핵심": ["정치", "법과 사회", "역사로 탐구하는 현대 세계"], "권장": ["세계시민과 지리", "사회문제 탐구", "영어 발표와 토론"]},
        "미디어커뮤니케이션학과": {"핵심": ["영어 발표와 토론", "매체 의사소통", "미디어 영어"], "권장": ["사회와 문화", "주제 탐구 독서", "소프트웨어와 생활"]},
        "행정학과": {"핵심": ["정치", "법과 사회", "사회문제 탐구"], "권장": ["사회와 문화", "확률과 통계", "실용 통계"]},
        "심리학과": {"핵심": ["인간과 심리", "확률과 통계", "사회문제 탐구"], "권장": ["생명과학", "세포와 물질대사", "실용 통계"]},
        "국어국문학과": {"핵심": ["주제 탐구 독서", "독서와 작문", "언어생활 탐구"], "권장": ["문학과 영상", "독서 토론과 글쓰기", "매체 의사소통"]},
        "영어영문학과": {"핵심": ["영어 발표와 토론", "영미 문학 읽기", "심화 영어"], "권장": ["영어 독해와 작문", "실생활 영어 회화", "미디어 영어"]},
        "사학과": {"핵심": ["세계사", "역사로 탐구하는 현대 세계", "인문학과 윤리"], "권장": ["도시의 미래 탐구", "여행지리", "독서 토론과 글쓰기"]},
        "철학과": {"핵심": ["현대사회와 윤리", "인문학과 윤리", "윤리와 사상"], "권장": ["윤리문제 탐구", "주제 탐구 독서", "독서 토론과 글쓰기"]},
        "법학과": {"핵심": ["정치", "법과 사회", "윤리문제 탐구"], "권장": ["사회와 문화", "사회문제 탐구", "독서 토론과 글쓰기"]},
        "사회학과": {"핵심": ["사회와 문화", "사회문제 탐구", "윤리문제 탐구"], "권장": ["정치", "확률과 통계", "실용 통계"]},
        "문헌정보학과": {"핵심": ["주제 탐구 독서", "데이터 과학", "소프트웨어와 생활"], "권장": ["독서와 작문", "독서 토론과 글쓰기"]},
        "지리학과": {"핵심": ["세계시민과 지리", "한국지리 탐구", "도시의 미래 탐구"], "권장": ["여행지리", "지구과학", "기후변화와 환경생태"]},
        "아동가족학과": {"핵심": ["사회와 문화", "인간과 심리", "사회문제 탐구"], "권장": ["현대사회와 윤리", "윤리문제 탐구"]},
        "소비자학과": {"핵심": ["사회와 문화", "경제 수학", "확률과 통계"], "권장": ["실용 통계", "인간과 심리", "사회문제 탐구"]},
        "무역학과": {"핵심": ["경제 수학", "확률과 통계", "세계사"], "권장": ["실용 통계", "세계시민과 지리", "실생활 영어 회화"]},
        "회계학과": {"핵심": ["경제 수학", "확률과 통계", "실용 통계"], "권장": ["데이터 과학", "수학과제 탐구"]}
    },
    "의학보건계열": {
        "의예과": {"핵심": ["생명과학", "세포와 물질대사", "생물의 유전"], "권장": ["화학", "화학 반응의 세계", "미적분II"]},
        "치의예과": {"핵심": ["생명과학", "세포와 물질대사", "미술 창작"], "권장": ["화학", "생물의 유전", "미적분II"]},
        "한의예과": {"핵심": ["생명과학", "세포와 물질대사", "인문학과 윤리"], "권장": ["지구과학", "윤리와 사상", "과학의 역사와 문화"]},
        "약학과": {"핵심": ["화학", "화학 반응의 세계", "세포와 물질대사"], "권장": ["생명과학", "생물의 유전", "미적분II"]},
        "간호학과": {"핵심": ["생명과학", "세포와 물질대사", "확률과 통계"], "권장": ["화학", "인간과 심리", "실생활 영어 회화"]},
        "생명공학과": {"핵심": ["생명과학", "세포와 물질대사", "화학 반응의 세계"], "권장": ["정보", "데이터 과학", "미적분II"]},
        "임상병리학과": {"핵심": ["생명과학", "세포와 물질대사", "화학"], "권장": ["화학 반응의 세계", "데이터 과학"]},
        "물리치료학과": {"핵심": ["생명과학", "세포와 물질대사", "물리학"], "권장": ["역학과 에너지", "인간과 심리"]}
    },
    "교육/기타계열": {
        "국어교육과": {"핵심": ["주제 탐구 독서", "독서와 작문", "언어생활 탐구"], "권장": ["인간과 심리", "독서 토론과 글쓰기"]},
        "영어교육과": {"핵심": ["영어 발표와 토론", "영미 문학 읽기", "심화 영어"], "권장": ["인간과 심리", "실생활 영어 회화"]},
        "수학교육과": {"핵심": ["미적분II", "확률과 통계", "수학과제 탐구"], "권장": ["기하", "실용 통계", "인간과 심리"]},
        "컴퓨터교육과": {"핵심": ["정보", "데이터 과학", "소프트웨어와 생활"], "권장": ["미적분II", "인간과 심리"]},
        "초등교육과": {"핵심": ["주제 탐구 독서", "확률과 통계", "인간과 심리"], "권장": ["음악 연주와 창작", "미술 창작", "사회문제 탐구"]},
        "교육학과": {"핵심": ["인간과 심리", "사회문제 탐구", "독서 토론과 글쓰기"], "권장": ["사회와 문화", "확률과 통계"]},
        "사회복지학과": {"핵심": ["사회문제 탐구", "윤리문제 탐구", "법과 사회"], "권장": ["사회와 문화", "인간과 심리"]},
        "의류학과": {"핵심": ["화학", "미술 창작", "사회문제 탐구"], "권장": ["물질과 에너지", "미술 감상과 비평", "경제 수학"]},
        "시각디자인학과": {"핵심": ["미술 창작", "미술 감상과 비평", "매체 의사소통"], "권장": ["소프트웨어와 생활", "문학과 영상"]},
        "체육학과": {"핵심": ["생명과학", "세포와 물질대사", "인간과 심리"], "권장": ["역학과 에너지", "사회문제 탐구"]},
        "음악학과": {"핵심": ["음악 연주와 창작", "음악 감상과 비평", "문학과 영상"], "권장": ["역사로 탐구하는 현대 세계", "인간과 심리"]},
        "연극영화학과": {"핵심": ["문학과 영상", "매체 의사소통", "미디어 영어"], "권장": ["미술 창작", "음악 연주와 창작"]}
    }
}

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
        reason = f"{major_name} 인프라의 핵심인 하드웨어 메커니즘 and 자연물리 법칙을 공학적으로 구현하는 기초 학문입니다."
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

def run_ai_diagnosis(selected_list, major_name, category_name, available_missing):
    rules = major_db[category_name][major_name]
    missing_cores = [sub for sub in rules.get("핵심", []) if sub in available_missing and sub not in selected_list]
    
    st.write("---")
    st.subheader("🤖 AI 진단 및 조정 권고 리포트")
    
    if len(missing_cores) == 0:
        st.success(f"✅ **[우수 조합]** 현재 선택안은 **{major_name}** 진학을 위한 핵심 교과목을 완벽히 충족합니다. 학생부 종합 전형 설계로 매우 우수합니다.")
    else:
        st.warning(f"⚠️ **[보완 필요 조합]** 선택하신 조합은 **{major_name}** 합격 확률을 높이기 위한 특정 교과목이 누락되어 보완이 필요합니다.")
        st.write(f"**미이수 핵심 과목**: {', '.join([f'**{m}**' for m in missing_cores])}")
        st.info(f"💡 **조정 추천**: 전공 연관성이 낮은 선택 과목을 최소화하고, 필수 전공 연계 교과인 **[{', '.join(missing_cores)}]** 과목으로 교체 조율하는 것을 권장합니다.")

# ==========================================
# 메인 컨트롤러: 학년 진입 세션 제어
# ==========================================
st.subheader("🎯 본인의 현재 학년을 선택해 주세요")
grade_auth = st.radio(
    "학년 선택에 따라 이수 과목 설계 범위 및 70:30 적합도 산출 가중치가 동적으로 변환됩니다.", 
    ["현재 1학년 (2학년 선택과목 설계 시기)", "현재 2학년 (3학년 선택과목 설계 시기)"],
    key="main_grade_timeline"
)

# 과거 이수 과목 배열 초기화
passed_subjects = []

# ------------------------------------------
# CASE A: 현재 1학년 프로세스 (고정형 3개 탭 아키텍처)
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
                t1_available = curriculum_db["2학년"]["1학기"]["영사과_택3"]["과목"] + curriculum_db["2학년"]["2학기"]["주요_택3"]["과목"]
                run_ai_diagnosis(t1_total, t1_maj, t1_cat, t1_available)

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
                t2_available = (curriculum_db["3학년"]["1학기"]["주요_택5"]["과목"] + curriculum_db["3학년"]["1학기"]["지정_택1"]["과목"] + 
                                curriculum_db["3학년"]["2학기"]["주요_택5"]["과목"] + curriculum_db["3학년"]["2학기"]["지정_택1"]["과목"])
                run_ai_diagnosis(t2_total, t1_maj, t1_cat, t2_available)

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
            st.dataframe(df_all, use_container_width=True, hide_index=True)

    with tab3:
        st.header("💡 1학년 사용자를 위한 시스템 가이드")
        st.info("현재 1학년 학생은 고교학점제 규정상 2학년과 3학년 과목 설계를 순차적으로 연속 진행해야 합니다. 1번 탭에서 2학년 및 3학년 시뮬레이션을 원스톱으로 마친 뒤, 2번 탭에서 전공에 필요한 22개 매칭 과목 리스트를 받아보십시오.")

# ------------------------------------------
# CASE B: 현재 2학년 프로세스 (고정형 3개 탭 아키텍처)
# ------------------------------------------
else:
    tab1, tab2, tab3 = st.tabs(["🎒 2학년 기이수 과목 확인", "📗 3학년 교육과정 설계", "🤖 3학년 맞춤 최적 패키지 추천"])
    
    with tab1:
        st.header("🎒 2학년 때 이수했던 과목을 체크해 주세요")
        st.write("3학년 과목의 30% 가중치인 '과목 연계성 점수'를 연산하기 위한 과거 이력 추적 장치입니다.")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("📌 **2학년 1학기 때 이수한 과목 체크**")
            for sub in curriculum_db["2학년"]["1학기"]["영사과_택3"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_1_g1_2_{sub}"): passed_subjects.append(sub)
            for sub in curriculum_db["2학년"]["1학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_1_g2_2_{sub}"): passed_subjects.append(sub)
        with col_p2:
            st.write("📌 **2학년 2학기 때 이수한 과목 체크**")
            for sub in curriculum_db["2학년"]["2학기"]["주요_택3"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_2_g3_2_{sub}"): passed_subjects.append(sub)
            for sub in curriculum_db["2학년"]["2학기"]["외국어_택1"]["과목"]:
                if st.checkbox(sub, key=f"passed_2_2_g4_2_{sub}"): passed_subjects.append(sub)
                
        st.success(f"현재 시스템이 인지한 2학년 이수 과목 개수: **{len(passed_subjects)}개**")
        st.info("💡 2학년 때 이수한 과목을 모두 체크하셨다면, 바로 2번 및 3번 탭으로 이동하여 3학년 과목을 설계해 주십시오.")

    with tab2:
        st.header("📋 3학년 수강 신청 시뮬레이션 (2학년 이수 연계 반영)")
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
            st.write("**[2학기] 예술 중 택 1 (각 3학점)**")
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
                t2_available = (curriculum_db["3학년"]["1학기"]["주요_택5"]["과목"] + curriculum_db["3학년"]["1학기"]["지정_택1"]["과목"] + 
                                curriculum_db["3학년"]["2학기"]["주요_택5"]["과목"] + curriculum_db["3학년"]["2학기"]["지정_택1"]["과목"])
                run_ai_diagnosis(t2_total, t2_3_maj, t2_3_cat, t2_available)

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
                    df_group = pd.DataFrame(group_records).sort_values(by="적합도 Git 점수", ascending=False, errors='ignore')
                    # 데이터프레임 키 정렬 안정화
                    df_group = df_group.sort_values(by="적합도 점수", ascending=False)
                    top_n = df_group.head(group_val["선택개수"])
                    final_recommended_records.extend(top_n.to_dict(orient="records"))
            
            df_all = pd.DataFrame(final_recommended_records).sort_values(by="적합도 점수", ascending=False).reset_index(drop=True)
            df_all.insert(0, "순위", list(range(1, len(df_all) + 1)))
            
            st.subheader(f"📋 3학년 맞춤 최적화 포트폴리오 (총 14개 과목 구성)")
            st.dataframe(df_all, use_container_width=True, hide_index=True)