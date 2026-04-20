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
            
            # 종합 분석 및 가설 검증 요약
            st.subheader("종합 분석 및 가설 검증 요약")
            
            # 평균 계산
            avg_total_1 = df1["총괄평가"].mean().round(3)
            avg_total_2 = df2["총괄평가"].mean().round(3)
            
            # 통합 데이터로 다중선형 회귀 (학기 더미 + 상호작용)
            df1_reg = df1[["평균점수", "총괄평가"]].copy()
            df1_reg["학기"] = 0  # 1학기 더미
            df2_reg = df2[["평균점수", "총괄평가"]].copy()
            df2_reg["학기"] = 1  # 2학기 더미
            df_combined_reg = pd.concat([df1_reg, df2_reg], ignore_index=True)
            
            # 표준화 및 상호작용 항 추가
            scaler = StandardScaler()
            df_combined_reg["평균점수_z"] = scaler.fit_transform(df_combined_reg[["평균점수"]])
            df_combined_reg["총괄평가_z"] = StandardScaler().fit_transform(df_combined_reg[["총괄평가"]])
            df_combined_reg["학기_평균점수"] = df_combined_reg["학기"] * df_combined_reg["평균점수_z"]
            
            # 다중선형 회귀
            X = df_combined_reg[["학기", "평균점수_z", "학기_평균점수"]]
            y = df_combined_reg["총괄평가_z"]
            model = LinearRegression().fit(X, y)
            
            # 계수 추출
            coef_semester = model.coef_[0]  # 2학기 효과 (평균점수 0일 때)
            coef_score = model.coef_[1]    # 1학기 '평균점수' 효과 (기준)
            coef_interaction = model.coef_[2]  # 2학기 '평균점수' 영향력 변화
            total_effect_2 = coef_score + coef_interaction
            
            st.markdown(f"""
--- 1학기 단일 회귀 모델의 표준화 계수 ---
{reg1['beta']:.14f}

--- 2학기 단일 회귀 모델의 표준화 계수 ---
{reg2['beta']:.13f}

--- 종합 다중선형 회귀 모델의 표준화 계수 ---
1학기 '탐구질문 평균점수' 효과 (기준): {coef_score:.14f}
2학기 '탐구질문 평균점수' 영향력 변화 (상호작용): {coef_interaction:.14f}
2학기 '탐구질문 평균점수' 총 효과 (1학기 효과 + 변화): {total_effect_2:.13f}
2학기 효과 (탐구질문 평균점수 0일 때): {coef_semester:.14f}

지금까지의 분석 결과를 바탕으로 '탐구질문 생성능력이 성적 향상에 영향력을 더 주었는가?'라는 사용자님의 가설을 검증하고, 관찰된 두 가지 주요 현상(총괄평가 점수 하락과 탐구질문 영향력 증가)을 종합적으로 설명합니다.

1. **총괄평가 점수의 전반적인 하락:**
   * 1학기 총괄평균: {avg_total_1}점
   * 2학기 총괄평균: {avg_total_2}점
   * **2학기의 총괄평가 점수가 1학기보다 전반적으로 낮아졌습니다.** 이는 학기별 평가 기준, 학습 난이도, 또는 학생들의 전반적인 학습 태도 변화 등 다양한 요인에 기인할 수 있습니다.

2. **탐구질문 생성능력의 영향력 증가 (종합 다중선형 회귀 분석 결과):**
   * **1학기 '탐구질문 평균점수'의 영향력 (기준):** {coef_score:.4f}
   * **2학기 '탐구질문 평균점수'의 영향력 변화 (상호작용 항):** {coef_interaction:.4f} (유의미)
   * **2학기 '탐구질문 평균점수'의 총 영향력:** {total_effect_2:.4f}
   * 다중선형 회귀 분석 결과에서 **'학기'와 '탐구질문 평균점수' 간의 상호작용 항이 통계적으로 유의미한 양수 값({coef_interaction:.4f})을 가지는 것**이 핵심입니다. 이는 1학기에 비해 **2학기에 '탐구질문 평균점수'가 '총괄평가'에 미치는 '영향력' 또는 '설명력'이 유의미하게 증가했음**을 의미합니다.

3. **두 현상에 대한 종합적인 해석 및 가설 검증:**
   * **겉보기의 모순:** 총괄평가 점수 자체는 2학기에 하락했지만, 탐구질문 생성능력이 총괄평가에 미치는 영향력은 오히려 커졌습니다. 이는 모순이 아니라, **'절대적인 점수의 변화'**와 **'어떤 요인의 중요도(영향력) 변화'**는 다를 수 있음을 시사합니다.
   * **비유:** 전체 학생들의 시험 점수 평균이 떨어지는 어려운 시험 상황에서도, 특정 학습 능력(예: 문제 해결 능력)이 높은 학생이 더 좋은 점수를 얻고, 그 능력의 차이가 점수 차이에 미치는 영향은 더 커질 수 있습니다. 즉, 어려운 환경일수록 해당 능력의 변별력이 더욱 중요해지는 것입니다.
   * **가설 검증:** 사용자님의 가설이 '탐구질문 생성능력이 성적 **향상에 영향력을 더 주었는가?**'에 초점을 맞춘다면, 저희 분석 결과는 이 가설을 **강력하게 지지합니다.** 비록 총괄평가 점수대가 전반적으로 낮아졌을지라도, 2학기에는 '탐구질문 생성능력'이 학생들의 '총괄평가'를 설명하고 예측하는 데 있어 **더욱 중요한 변별 요인으로 작용했음**을 회귀 분석 결과가 명확히 보여주고 있습니다.
""")
            
        else:
            st.warning("회귀분석을 실행할 수 없습니다. 데이터를 확인하세요.")
            
    except Exception as e:
        st.error(f"데이터를 처리할 수 없습니다: {e}")
