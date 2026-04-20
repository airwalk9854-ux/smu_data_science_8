import streamlit as st
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# 페이지 설정
st.set_page_config(page_title="탐구질문 관리", layout="wide")

st.title("📚 탐구질문 만들기")

# 탭 생성
tab1, tab2 = st.tabs(["1학기", "2학기"])

# 데이터 파일 경로
data_dir = "data"
file_semester1 = os.path.join(data_dir, "1학기 탐구질문 만들기.xlsx")
file_semester2 = os.path.join(data_dir, "2학기 탐구질문 만들기.xlsx")


def standardized_regression(df, x_col, y_col):
    if x_col not in df.columns or y_col not in df.columns:
        return None

    X = df[[x_col]].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(df[y_col], errors="coerce")
    valid = X[x_col].notna() & y.notna()
    if valid.sum() < 2:
        return None

    Xs = StandardScaler().fit_transform(X.loc[valid])
    ys = StandardScaler().fit_transform(y.loc[valid].values.reshape(-1, 1))
    model = LinearRegression().fit(Xs, ys)
    return {
        "beta": float(model.coef_[0][0]),
        "intercept": float(model.intercept_[0]),
        "r2": float(model.score(Xs, ys)),
        "corr": float(X.loc[valid, x_col].corr(y.loc[valid]))
    }

# 1학기 탭
with tab1:
    st.header("1학기 탐구질문 만들기")
    try:
        df1 = pd.read_excel(file_semester1)
        score_cols = ["탐구질문 만들기1", "탐구질문 만들기2", "탐구질문 만들기3", "탐구질문 만들기4"]
        if all(col in df1.columns for col in score_cols):
            df1["평균점수"] = df1[score_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1).round(2)
        else:
            missing = [col for col in score_cols if col not in df1.columns]
            st.warning(f"평균점수를 계산할 수 없는 열이 있습니다: {', '.join(missing)}")

        st.write(f"총 {len(df1)}개의 항목")
        st.dataframe(df1, use_container_width=True)

        regression1 = standardized_regression(df1, "평균점수", "총괄평가")
        if regression1 is not None:
            st.subheader("회귀 분석 결과")
            st.markdown(
                f"- 표준화 계수 (beta): **{regression1['beta']:.4f}**\n"
                f"- 결정계수 (R²): **{regression1['r2']:.4f}**\n"
                f"- 상관계수: **{regression1['corr']:.4f}**\n"
                f"- 표준화 회귀식: Z(총괄평가) = {regression1['beta']:.4f} × Z(평균점수) + {regression1['intercept']:.4f}"
            )
        else:
            st.warning("회귀 분석을 실행할 수 없습니다. '평균점수' 또는 '총괄평가' 열을 확인하세요.")
        
        # 다운로드 버튼
        with open(file_semester1, 'rb') as excel_file1:
            st.download_button(
                label="1학기 파일 다운로드",
                data=excel_file1,
                file_name="1학기 탐구질문 만들기.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"파일을 읽을 수 없습니다: {e}")

# 2학기 탭
with tab2:
    st.header("2학기 탐구질문 만들기")
    try:
        df2 = pd.read_excel(file_semester2)
        score_cols = ["탐구질문 만들기1", "탐구질문 만들기2", "탐구질문 만들기3", "탐구질문 만들기4"]
        if all(col in df2.columns for col in score_cols):
            df2["평균점수"] = df2[score_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1).round(2)
        else:
            missing = [col for col in score_cols if col not in df2.columns]
            st.warning(f"평균점수를 계산할 수 없는 열이 있습니다: {', '.join(missing)}")

        st.write(f"총 {len(df2)}개의 항목")
        st.dataframe(df2, use_container_width=True)

        regression2 = standardized_regression(df2, "평균점수", "총괄평가")
        if regression2 is not None:
            st.subheader("회귀 분석 결과")
            st.markdown(
                f"- 표준화 계수 (beta): **{regression2['beta']:.4f}**\n"
                f"- 결정계수 (R²): **{regression2['r2']:.4f}**\n"
                f"- 상관계수: **{regression2['corr']:.4f}**\n"
                f"- 표준화 회귀식: Z(총괄평가) = {regression2['beta']:.4f} × Z(평균점수) + {regression2['intercept']:.4f}"
            )
        else:
            st.warning("회귀 분석을 실행할 수 없습니다. '평균점수' 또는 '총괄평가' 열을 확인하세요.")
        
        # 다운로드 버튼
        with open(file_semester2, 'rb') as excel_file2:
            st.download_button(
                label="2학기 파일 다운로드",
                data=excel_file2,
                file_name="2학기 탐구질문 만들기.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"파일을 읽을 수 없습니다: {e}")
