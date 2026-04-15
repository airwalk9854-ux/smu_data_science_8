import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="탐구질문 관리", layout="wide")

st.title("📚 탐구질문 만들기")

# 탭 생성
tab1, tab2 = st.tabs(["1학기", "2학기"])

# 데이터 파일 경로
data_dir = "data"
file_semester1 = os.path.join(data_dir, "1학기 탐구질문 만들기.xlsx")
file_semester2 = os.path.join(data_dir, "2학기 탐구질문 만들기.xlsx")

# 1학기 탭
with tab1:
    st.header("1학기 탐구질문 만들기")
    try:
        df1 = pd.read_excel(file_semester1)
        st.write(f"총 {len(df1)}개의 항목")
        st.dataframe(df1, use_container_width=True)
        
        # 다운로드 버튼
        excel_file1 = open(file_semester1, 'rb')
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
        st.write(f"총 {len(df2)}개의 항목")
        st.dataframe(df2, use_container_width=True)
        
        # 다운로드 버튼
        excel_file2 = open(file_semester2, 'rb')
        st.download_button(
            label="2학기 파일 다운로드",
            data=excel_file2,
            file_name="2학기 탐구질문 만들기.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"파일을 읽을 수 없습니다: {e}")
