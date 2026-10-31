import pandas as pd
import streamlit as st

st.title("Widget & 파일 업로드")
st.header("기본 위젯")
name = st.text_input("이름")
subject = st.selectbox("학습 주제", ["Streamlit", "LangChain", "AI Agent"])
if st.button("인사하기"):
    st.success(f"{name or '방문자'}님, 반갑습니다! {subject}을 함께 배워요.")


def show_excel(uploaded_file):
    """업로드한 엑셀의 시트 목록과 선택한 시트를 표시합니다."""
    try:
        with pd.ExcelFile(uploaded_file) as workbook:
            sheet = st.selectbox(
                "시트 선택", workbook.sheet_names, key=f"sheet_{uploaded_file.file_id}"
            )
            frame = pd.read_excel(workbook, sheet_name=sheet)
        st.caption(f"{len(frame):,}행 · {len(frame.columns):,}열")
        st.dataframe(frame, width="stretch")
    except Exception:
        st.error("엑셀 파일을 읽을 수 없습니다. 암호화되지 않은 정상적인 .xlsx 또는 .xls 파일인지 확인하세요.")


st.header("단일 파일 업로드")
single = st.file_uploader("엑셀 파일을 선택하세요", type=["xlsx", "xls"], key="single")
if single is not None:
    show_excel(single)

st.header("복수 파일 업로드")
multiple = st.file_uploader(
    "엑셀 파일을 여러 개 선택하세요",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    key="multiple",
)
for uploaded in multiple:
    with st.expander(uploaded.name, expanded=True):
        show_excel(uploaded)
