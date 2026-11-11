# 🎓 캠퍼스 생활 설문조사 분석 대시보드 (Campus Life Analysis)

Streamlit 기반의 데이터 분석 웹 애플리케이션으로, 대학생들의 학과별 생활 습관(통학, 공부, 수면, 스마트폰 사용)과 학교생활 만족도 간의 관계를 분석하고 visualizes(시각화)하는 프로젝트입니다.

---

## 📌 주요 기능 (Features)

1. **📁 데이터 업로드 및 전처리**
   - CSV 파일(`campus_life.csv`) 업로드 지원
   - 수치형 데이터의 결측치(NaN)를 평균값으로 자동 보정
   - 텍스트/범주형 데이터의 결측치 기본값 대체 처리

2. **🔎 학과별 필터링 기능**
   - 사이드바 메뉴를 통해 특정 학과 또는 전체 학과 데이터 선택 가능

3. **📊 학과별 생활 습관 비교**
   - 학과에 따른 평균 통학시간, 공부시간, 스마트폰 사용시간, 수면시간을 막대그래프로 비교 시각화

4. **🔍 학교생활 만족도 관련성 분석**
   - 주요 생활 습관과 학교생활 만족도 간의 관계를 산점도(Scatter Plot)로 시각화하여 관련성 파악

5. **☁️ 한줄의견 키워드 워드클라우드**
   - 설문 참여자들의 한줄의견 텍스트 데이터를 수집하여 주요 단어 빈도수를 워드클라우드로 시각화

---

## 🛠️ 기술 스택 (Tech Stack)

- **Language:** Python 3.11+
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn, WordCloud

---

## 📂 프로젝트 구조 (Project Structure)

```text
├── app.py                # Main Streamlit 애플리케이션 코드
├── campus_life.csv       # 설문조사 샘플 데이터셋
├── NanumGothic.ttf       # 한글 깨짐 방지용 폰트 파일
├── requirements.txt      # 프로젝트 의존성 라이브러리 목록
└── README.md             # 프로젝트 설명서 (본 파일)
```

---

## 🚀 로컬 실행 방법 (Local Run)

### 1. 저장소 클론 (Clone)
```bash
git clone https://github.com/사용자계정/저장소이름.git
cd 저장소이름
```

### 2. 가상환경 생성 및 활성화 (선택)
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. 라이브러리 설치 (Install Requirements)
```bash
pip install -r requirements.txt
```

### 4. Streamlit 앱 실행 (Run App)
```bash
streamlit run app.py
```

---

## 📝 폰트 관련 참고사항
Matplotlib 및 WordCloud 시각화 시 한글 폰트 깨짐 현상을 방지하기 위해 프로젝트 루트 경로에 `NanumGothic.ttf` 파일이 필요합니다.