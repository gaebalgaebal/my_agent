# my_agent

AI 에이전트 프로젝트 저장소입니다.

Streamlit 강의자료의 기초 챗봇과 환율 조회 웹앱 미니 프로젝트를 구현했습니다.

## 실행 (PowerShell / Python 3.10 이상)

```powershell
cd 'E:\26-2 생성형 인공지능 활용\my_agent'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
.\.venv\Scripts\python.exe -m streamlit run app.py
```

`.env`의 `OPENAI_API_KEY=` 뒤에 본인의 API 키를 입력하세요.
이미 `.env`가 있다면 복사 단계는 건너뛰세요. 키 변경 후 앱을 다시 실행하세요.
`OPENAI_MODEL` 기본값은 강의자료의 `gpt-5.4-mini`이며, 계정에서 사용 가능한 모델로 바꿀 수 있습니다.
API 호출에는 해당 계정의 사용 요금이 발생할 수 있습니다.
`.env`와 `.streamlit/secrets.toml`은 Git에서 제외됩니다.

## 구현 내용

- `app.py`: `st.Page`, `st.navigation`을 이용한 4개 페이지 이동
- `page_1.py`: `st.chat_input`, `st.chat_message`, `st.session_state` 대화 기록,
  LangChain `init_chat_model`과 `invoke` 기반 AI 응답
- `page_2.py`: title, header, write, markdown, badge, caption 실습
- `page_3.py`: 버튼·입력·선택 위젯, 단일/복수 엑셀(.xlsx, .xls) 업로드 및 시트 조회

API 키 없이도 사이드바의 **기초 인사 실습**으로 대화 기록 유지를 확인할 수 있습니다.
대화 기록은 현재 브라우저 세션에서 유지되며 영구 저장하지 않습니다.
엑셀 업로드는 표 조회용이며 챗봇에 전달하지 않습니다.

강의 코드의 `response.output_text`는 LangChain AIMessage에 맞게 `response.text`로 수정했습니다.
대화 문맥을 유지하도록 현재 대화 기록 전체를 모델에 전달합니다.
배포는 진행하지 않았습니다.

## 환율 조회 웹앱

상단의 **환율 조회** 페이지에서 기준 통화, 대상 통화, 금액을 선택하고
**환율 조회** 버튼을 누르면 최신 환율과 환산 금액, API 데이터 기준일을 표시합니다.
Frankfurter 공개 v2 API를 사용하며 API 키나 OpenAI 설정이 필요하지 않습니다.
통화 목록은 하루, 환율은 1시간 캐시합니다. 동일 통화는 API 호출 없이 1로 환산합니다.
조회 실패 시 오류 메시지를 표시하며 이전 결과를 지웁니다.
일별 참고 환율로 은행의 실제 환전 수수료나 매매 환율은 포함하지 않습니다.

- `page_4.py`: 환율 조회 화면
- `exchange.py`: 통화 목록 및 환율 HTTP 조회 (15초 타임아웃)
- API 문서: https://frankfurter.dev/

## 검증

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

페이지 이동, 인사 실습의 대화 기록과 초기화, 단일·복수 엑셀 조회,
모의 모델을 이용한 대화 문맥 전달을 검증합니다. 실제 API 호출은 하지 않습니다.
환율 테스트는 금액 환산, 동일 통화, 통신 실패, 잘못된 환율 응답도 검증합니다.
