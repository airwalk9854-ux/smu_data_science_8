import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

# 한글 폰트 설정
# Noto Sans CJK 폰트 파일 경로 (로컬 또는 다운로드된 파일)
noto_font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
local_font_path = 'NotoSansCJK-Regular.ttc'  # 앱 디렉토리에 다운로드된 폰트

if os.path.exists(noto_font_path):
    fm.fontManager.addfont(noto_font_path)
    mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
elif os.path.exists(local_font_path):
    fm.fontManager.addfont(local_font_path)
    mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
else:
    # 폰트가 없으면 기본 폰트 사용 (한글 지원 안 됨)
    mpl.rcParams['font.family'] = 'DejaVu Sans'

mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

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
            
            # 산점도 비교 (통합)
            st.subheader("산점도 비교")
            
            # 1학기와 2학기 데이터 통합
            df1_plot = df1[["평균점수", "총괄평가"]].copy()
            df1_plot["학기"] = "1학기"
            df2_plot = df2[["평균점수", "총괄평가"]].copy()
            df2_plot["학기"] = "2학기"
            df_combined_plot = pd.concat([df1_plot, df2_plot], ignore_index=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # 1학기 점
            mask1 = df_combined_plot["학기"] == "1학기"
            ax.scatter(df_combined_plot.loc[mask1, "평균점수"], 
                      df_combined_plot.loc[mask1, "총괄평가"], 
                      alpha=0.6, color='#FF6B6B', s=50, label="1학기")
            
            # 2학기 점
            mask2 = df_combined_plot["학기"] == "2학기"
            ax.scatter(df_combined_plot.loc[mask2, "평균점수"], 
                      df_combined_plot.loc[mask2, "총괄평가"], 
                      alpha=0.6, color='#4ECDC4', s=50, label="2학기")
            
            # 1학기 회귀선
            x1 = df1["평균점수"].values
            y1 = df1["총괄평가"].values
            z1 = np.polyfit(x1, y1, 1)
            p1 = np.poly1d(z1)
            x_line1 = np.linspace(x1.min(), x1.max(), 100)
            ax.plot(x_line1, p1(x_line1), "r-", linewidth=2, alpha=0.8)
            
            # 2학기 회귀선
            x2 = df2["평균점수"].values
            y2 = df2["총괄평가"].values
            z2 = np.polyfit(x2, y2, 1)
            p2 = np.poly1d(z2)
            x_line2 = np.linspace(x2.min(), x2.max(), 100)
            ax.plot(x_line2, p2(x_line2), "b-", linewidth=2, alpha=0.8)
            
            ax.set_xlabel("탐구질문 만들기 평균점수", fontsize=11, fontweight='bold')
            ax.set_ylabel("총괄평가 점수", fontsize=11, fontweight='bold')
            ax.set_title("1학기 vs 2학기: 평균점수 vs 총괄평가 비교", fontsize=12, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
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
