import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="탐구질문 관리", layout="wide")

st.title("📚 탐구질문 만들기")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["1학기", "2학기", "회귀분석 비교"])

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
        
        # 표시할 열 필터링 및 이름 변경
        display_cols = ["학년", "학급", "번호", "평균", "총괄평가"]
        df1_display = df1[display_cols].copy()
        df1_display = df1_display.rename(columns={"평균": "탐구질문 만들기 평균점수"})

        avg_score = df1_display["탐구질문 만들기 평균점수"].mean().round(2)
        avg_total = df1_display["총괄평가"].mean().round(2)
        footer_row = pd.DataFrame([
            {"학년": "", "학급": "", "번호": "평균", "탐구질문 만들기 평균점수": avg_score, "총괄평가": avg_total}
        ])
        df1_display = pd.concat([df1_display, footer_row], ignore_index=True)
        
        st.dataframe(df1_display, use_container_width=True)

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
        
        # 표시할 열 필터링 및 이름 변경
        display_cols = ["학년", "학급", "번호", "평균", "총괄평가"]
        df2_display = df2[display_cols].copy()
        df2_display = df2_display.rename(columns={"평균": "탐구질문 만들기 평균점수"})

        avg_score = df2_display["탐구질문 만들기 평균점수"].mean().round(2)
        avg_total = df2_display["총괄평가"].mean().round(2)
        footer_row = pd.DataFrame([
            {"학년": "", "학급": "", "번호": "평균", "탐구질문 만들기 평균점수": avg_score, "총괄평가": avg_total}
        ])
        df2_display = pd.concat([df2_display, footer_row], ignore_index=True)
        
        st.dataframe(df2_display, use_container_width=True)

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

# 회귀분석 비교 탭
with tab3:
    st.header("회귀분석 결과 비교")
    try:
        # 데이터 로드
        df1 = pd.read_excel(file_semester1)
        df2 = pd.read_excel(file_semester2)
        
        # 평균점수 계산
        score_cols = ["탐구질문 만들기1", "탐구질문 만들기2", "탐구질문 만들기3", "탐구질문 만들기4"]
        df1["평균점수"] = df1[score_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1).round(2)
        df2["평균점수"] = df2[score_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1).round(2)
        
        # 각 학기 회귀분석
        reg1 = standardized_regression(df1, "평균점수", "총괄평가")
        reg2 = standardized_regression(df2, "평균점수", "총괄평가")
        
        if reg1 is not None and reg2 is not None:
            # 회귀분석 결과 비교 테이블
            st.subheader("회귀분석 결과 비교")
            comparison_data = pd.DataFrame([
                {"학기": "1학기", "표준화계수(beta)": reg1['beta'], "결정계수(R²)": reg1['r2'], "상관계수": reg1['corr']},
                {"학기": "2학기", "표준화계수(beta)": reg2['beta'], "결정계수(R²)": reg2['r2'], "상관계수": reg2['corr']}
            ])
            st.dataframe(comparison_data, use_container_width=True)
            
            # 회귀 계수 비교 그래프
            st.subheader("회귀 분석 지표 비교")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chart_data = pd.DataFrame({
                    "학기": ["1학기", "2학기"],
                    "표준화계수(Beta)": [reg1['beta'], reg2['beta']]
                })
                st.bar_chart(chart_data.set_index("학기"))
                st.metric("표준화 계수 (Beta)", f"1학기: {reg1['beta']:.4f} vs 2학기: {reg2['beta']:.4f}")
            
            with col2:
                chart_data = pd.DataFrame({
                    "학기": ["1학기", "2학기"],
                    "결정계수(R²)": [reg1['r2'], reg2['r2']]
                })
                st.bar_chart(chart_data.set_index("학기"))
                st.metric("결정계수 (R²)", f"1학기: {reg1['r2']:.4f} vs 2학기: {reg2['r2']:.4f}")
            
            with col3:
                chart_data = pd.DataFrame({
                    "학기": ["1학기", "2학기"],
                    "상관계수": [reg1['corr'], reg2['corr']]
                })
                st.bar_chart(chart_data.set_index("학기"))
                st.metric("상관계수", f"1학기: {reg1['corr']:.4f} vs 2학기: {reg2['corr']:.4f}")
            
            # 산점도 비교
            st.subheader("산점도 비교")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1학기: 평균점수 vs 총괄평가**")
                # 1학기 산점도와 회귀선
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                x1 = df1["평균점수"].values
                y1 = df1["총괄평가"].values
                ax1.scatter(x1, y1, alpha=0.6, color='#FF6B6B', s=50)
                
                # 회귀선 그리기
                z = np.polyfit(x1, y1, 1)
                p = np.poly1d(z)
                x_line = np.linspace(x1.min(), x1.max(), 100)
                ax1.plot(x_line, p(x_line), "r-", linewidth=2, label="회귀선")
                
                ax1.set_xlabel("탐구질문 만들기 평균점수", fontsize=10)
                ax1.set_ylabel("총괄평가 점수", fontsize=10)
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                st.pyplot(fig1)
            
            with col2:
                st.write("**2학기: 평균점수 vs 총괄평가**")
                # 2학기 산점도와 회귀선
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                x2 = df2["평균점수"].values
                y2 = df2["총괄평가"].values
                ax2.scatter(x2, y2, alpha=0.6, color='#4ECDC4', s=50)
                
                # 회귀선 그리기
                z = np.polyfit(x2, y2, 1)
                p = np.poly1d(z)
                x_line = np.linspace(x2.min(), x2.max(), 100)
                ax2.plot(x_line, p(x_line), "b-", linewidth=2, label="회귀선")
                
                ax2.set_xlabel("탐구질문 만들기 평균점수", fontsize=10)
                ax2.set_ylabel("총괄평가 점수", fontsize=10)
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                st.pyplot(fig2)
            
            # 분석 요약
            st.subheader("분석 요약")
            if reg1['beta'] > reg2['beta']:
                summary = f"1학기의 표준화 계수({reg1['beta']:.4f})가 2학기({reg2['beta']:.4f})보다 크므로, 1학기에서 평균점수가 총괄평가에 미치는 영향이 더 큽니다."
            else:
                summary = f"2학기의 표준화 계수({reg2['beta']:.4f})가 1학기({reg1['beta']:.4f})보다 크므로, 2학기에서 평균점수가 총괄평가에 미치는 영향이 더 큽니다."
            st.info(summary)
            
        else:
            st.warning("회귀분석을 실행할 수 없습니다. 데이터를 확인하세요.")
            
    except Exception as e:
        st.error(f"데이터를 처리할 수 없습니다: {e}")
