import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 한글 폰트 설정 (NanumGothic.ttf 사용)
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="캠퍼스 생활 설문조사 분석", layout="wide")

st.title("🎓 캠퍼스 생활 설문조사 분석 프로그램")
st.write("파이썬 초보자도 쉽게 이해할 수 있는 설문조사 데이터 분석 대시보드입니다.")


# -------------------------------------------------------------------------
# 1. 파일 업로드 및 데이터 전처리 함수
# -------------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_data(uploaded_file):
    """
    CSV 파일을 읽어오고 결측치 및 잘못된 값을 전처리하는 함수
    """
    df = pd.read_csv(uploaded_file)

    # 예시 컬럼 가정: 학과, 통학시간, 공부시간, 스마트폰시간, 수면시간, 만족도, 한줄의견
    # 결측치 처리: 수치형 데이터는 평균값으로 대체, 범주형/텍스트는 '기타' 또는 빈 문자열로 대체
    numeric_cols = ['통학시간', '공부시간', '스마트폰시간', '수면시간', '만족도']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # 숫자가 아닌 값은 NaN으로 변환
            df[col].fillna(df[col].mean(), inplace=True)  # 결측치 평균값 대입

    if '한줄의견' in df.columns:
        df['한줄의견'] = df['한줄의견'].fillna("의견 없음")

    if '학과' in df.columns:
        df['학과'] = df['학과'].fillna("미분류")

    return df


# -------------------------------------------------------------------------
# 3. 학과별 생활 습관 비교 시각화 함수
# -------------------------------------------------------------------------
def plot_lifestyle_comparison(df):
    """
    학과별 평균 생활 습관(공부, 수면, 스마트폰 등)을 비교하는 막대 그래프 생성 함수
    """
    st.subheader("📊 3. 학과별 생활 습관 비교")

    habits = ['통학시간', '공부시간', '스마트폰시간', '수면시간']
    available_habits = [h for h in habits if h in df.columns]

    if available_habits:
        # 학과별 평균 계산
        dept_avg = df.groupby('학과')[available_habits].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 5))
        dept_avg.set_index('학과')[available_habits].plot(kind='bar', ax=ax, width=0.8)

        ax.set_title("학과별 평균 생활 습관 비교", fontsize=14)
        ax.set_xlabel("학과", fontsize=12)
        ax.set_ylabel("시간 (시간)", fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title="생활 습관")
        st.pyplot(fig)
    else:
        st.warning("비교할 생활 습관 데이터 컬럼이 부족합니다.")


# -------------------------------------------------------------------------
# 4. 만족도 관련성 분석 및 시각화 함수
# -------------------------------------------------------------------------
def plot_satisfaction_correlation(df):
    """
    공부시간, 수면시간 등과 학교생활 만족도의 관계를 산점도로 분석하는 함수
    """
    st.subheader("🔍 4. 생활 습관과 학교생활 만족도 관계 분석")

    if '만족도' in df.columns:
        target_habit = st.selectbox("비교할 생활 습관을 선택하세요:", ['공부시간', '수면시간', '스마트폰시간', '통학시간'])

        if target_habit in df.columns:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.scatterplot(data=df, x=target_habit, y='만족도', hue='학과', s=100, ax=ax)
            ax.set_title(f"{target_habit}과 학교생활 만족도의 관계", fontsize=14)
            st.pyplot(fig)
    else:
        st.warning("'만족도' 데이터가 존재하지 않습니다.")


# -------------------------------------------------------------------------
# 5. 한줄의견 텍스트 분석 및 워드클라우드 시각화 함수
# -------------------------------------------------------------------------
def visualize_wordcloud(df):
    """
    한줄의견 텍스트를 모아 워드클라우드로 시각화하는 함수
    """
    st.subheader("☁️ 5. 한줄의견 키워드 워드클라우드")

    if '한줄의견' in df.columns:
        text_data = " ".join(df['한줄의견'].astype(str).tolist())

        if text_data.strip():
            # NanumGothic.ttf 폰트 경로 지정 (환경에 맞게 수정 가능)
            font_path = "NanumGothic.ttf"

            try:
                wc = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(text_data)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"워드클라우드 생성 중 오류가 발생했습니다 (폰트 파일 확인 필요): {e}")
        else:
            st.info("분석할 텍스트 의견이 없습니다.")


# -------------------------------------------------------------------------
# 메인 실행 흐름 (화면 레이아웃 순서 배치)
# -------------------------------------------------------------------------
def main():
    # 1. CSV 파일 업로드
    st.sidebar.header("📁 데이터 파일 업로드")
    uploaded_file = st.sidebar.file_uploader("campus_life.csv 파일을 업로드하세요", type=["csv"])

    if uploaded_file is not None:
        # 데이터 로드 및 전처리
        df = load_and_preprocess_data(uploaded_file)

        # 2. 학과 선택 필터 (사이드바 배치)
        st.sidebar.header("🔎 필터 옵션")
        departments = ['전체'] + list(df['학과'].unique())
        selected_dept = st.sidebar.selectbox("학과 선택", departments)

        # 필터 적용
        if selected_dept != '전체':
            filtered_df = df[df['학과'] == selected_dept]
        else:
            filtered_df = df

        # 3. 데이터 전처리 결과 화면 표시
        st.subheader("📋 3. 데이터 전처리 결과 (상위 5행)")
        st.dataframe(filtered_df.head())
        st.write(f"총 데이터 건수: **{len(filtered_df)}건** (결측치 정제 완료)")

        st.markdown("---")

        # 4. 학과별 생활 습관 비교 시각화
        plot_lifestyle_comparison(filtered_df)

        st.markdown("---")

        # 5. 만족도 관련성 분석
        plot_satisfaction_correlation(filtered_df)

        st.markdown("---")

        # 6. 한줄의견 단어 분석 및 워드클라우드
        visualize_wordcloud(filtered_df)

    else:
        st.info("👈 사이드바에서 `campus_life.csv` 파일을 업로드하면 분석 화면이 나타납니다.")


if __name__ == "__main__":
    main()
