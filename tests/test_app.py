import os
from io import BytesIO
import unittest
from pathlib import Path
from unittest.mock import patch

from langchain_core.messages import AIMessage
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class AppTests(unittest.TestCase):
    def test_excel_uploads(self):
        def upload(file_id):
            buffer = BytesIO()
            pd.DataFrame({"이름": ["테스트"], "값": [10]}).to_excel(buffer, index=False)
            buffer.seek(0)
            buffer.name = "sample.xlsx"
            buffer.file_id = file_id
            return buffer

        with patch("streamlit.file_uploader", side_effect=[upload("one"), [upload("two"), upload("three")]]):
            app = AppTest.from_file(str(ROOT / "page_3.py")).run(timeout=30)
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertEqual(len(app.dataframe), 3)
            self.assertEqual(app.dataframe[0].value.iloc[0]["값"], 10)

    def test_pages_and_greeting_history(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
            self.assertFalse(app.exception)
            self.assertTrue(app.chat_input[0].disabled)
            app.sidebar.radio[0].set_value("기초 인사 실습").run()
            app.chat_input[0].set_value("안녕하세요").run()
            app.chat_input[0].set_value("두 번째 대화").run()
            self.assertEqual(len(app.session_state.messages), 4)
            app.switch_page("page_2.py").run()
            self.assertFalse(app.exception)
            app.switch_page("page_3.py").run()
            self.assertFalse(app.exception)
            app.text_input[0].set_value("학생").run()
            app.button[0].click().run()
            self.assertIn("학생", app.success[0].value)
            app.switch_page("page_1.py").run()
            self.assertEqual(len(app.session_state.messages), 4)
            app.sidebar.button[0].click().run()
            self.assertEqual(app.session_state.messages, [])

    def test_model_receives_history(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch(
            "langchain.chat_models.init_chat_model"
        ) as factory:
            factory.return_value.invoke.return_value = AIMessage(content="테스트 응답")
            app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
            app.chat_input[0].set_value("첫 질문").run()
            app.chat_input[0].set_value("이전 질문은?").run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.messages[-1]["content"], "테스트 응답")
            self.assertEqual(factory.return_value.invoke.call_args.args[0][0]["content"], "첫 질문")


if __name__ == "__main__":
    unittest.main()
