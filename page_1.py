import os

import streamlit as st
from langchain.chat_models import init_chat_model
from openai import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError

st.title("AI Agent")
st.caption("LangChain과 Streamlit으로 만드는 기초 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = []

mode = st.sidebar.radio("응답 방식", ["AI 챗봇", "기초 인사 실습"])
model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
st.sidebar.caption(f"모델: {model_name}")
if st.sidebar.button("대화 초기화"):
    st.session_state.messages = []

has_key = bool(os.getenv("OPENAI_API_KEY", "").strip())
if mode == "AI 챗봇" and not has_key:
    st.info("AI 응답을 사용하려면 .env에 OPENAI_API_KEY를 설정하고 앱을 다시 실행하세요. 기초 인사 실습은 키 없이 사용할 수 있습니다.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "무엇을 도와드릴까요?",
    disabled=mode == "AI 챗봇" and not has_key,
)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하고 있습니다..."):
                if mode == "기초 인사 실습":
                    answer = "반갑습니다."
                else:
                    model = init_chat_model(
                        model_name, model_provider="openai", timeout=60, max_retries=1
                    )
                    response = model.invoke(st.session_state.messages)
                    # LangChain invoke는 AIMessage를 반환합니다.
                    answer = response.text
                    if not answer.strip():
                        raise ValueError("empty response")
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except (AuthenticationError, RateLimitError, APIConnectionError, APIStatusError, ValueError) as error:
        # 원본 예외에는 요청 정보가 포함될 수 있어 화면에 노출하지 않습니다.
        st.session_state.messages.pop()
        if isinstance(error, AuthenticationError):
            st.error("API 키를 확인하세요. .env 수정 후 앱을 다시 실행하세요.")
        elif isinstance(error, RateLimitError):
            st.error("API 사용 한도 또는 요청 제한을 확인하고 다시 시도하세요.")
        else:
            st.error("답변을 받지 못했습니다. 네트워크와 모델 설정을 확인한 뒤 다시 입력하세요.")
