from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))
st.set_page_config(page_title="AI Agent", page_icon="🤖")

pages = st.navigation(
    [
        st.Page("page_1.py", title="챗봇", icon="💬"),
        st.Page("page_2.py", title="텍스트 예제", icon="📝"),
        st.Page("page_3.py", title="엑셀 조회", icon="📂"),
        st.Page("page_4.py", title="환율 조회", icon="💱"),
    ],
    position="top",
)
pages.run()
