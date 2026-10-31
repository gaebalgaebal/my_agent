# my_agent

Streamlit 기반 챗봇 · 엑셀 조회 · 환율 계산 앱

## 실행

Python 3.10 이상, Windows 기준입니다.

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
```

`.env.example`을 `.env`로 복사하고 챗봇용 `OPENAI_API_KEY`를 입력하세요.
이미 `.env`가 있다면 그대로 사용하세요. 환율 조회에는 키가 필요 없습니다.

```bash
./.venv/Scripts/python.exe -m streamlit run app.py
```

## 기능

- 챗봇: AI 응답, 대화 기록, 초기화
- 텍스트: Streamlit 텍스트 요소 예제
- 엑셀: 단일·복수 파일 업로드 및 시트 조회
- 환율: 통화 선택, 금액 환산, 기준일 표시 ([Frankfurter](https://frankfurter.dev/))

## 테스트

```bash
./.venv/Scripts/python.exe -m unittest discover -s tests -v
```
