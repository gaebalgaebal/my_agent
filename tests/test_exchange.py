import unittest
from pathlib import Path
from unittest.mock import patch

import requests
import streamlit as st
from streamlit.testing.v1 import AppTest

from exchange import get_rate

ROOT = Path(__file__).resolve().parents[1]


class ExchangeTests(unittest.TestCase):
    def setUp(self):
        st.cache_data.clear()

    def test_conversion_and_same_currency(self):
        with patch("exchange.get_currencies", return_value={"USD": "US Dollar", "KRW": "Won"}), patch(
            "exchange.get_rate", return_value={"rate": 1300.0, "date": "2026-10-30"}
        ) as rate:
            app = AppTest.from_file(str(ROOT / "page_4.py")).run()
            app.number_input[0].set_value(10)
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.metric[0].value, "13,000.00 KRW")
            app.selectbox[1].set_value("USD")
            app.button[0].click().run()
            self.assertEqual(app.metric[0].value, "10.00 USD")
            self.assertEqual(rate.call_count, 1)

    def test_failure_removes_previous_result(self):
        with patch("exchange.get_currencies", return_value={"USD": "Dollar", "KRW": "Won"}), patch(
            "exchange.get_rate", side_effect=requests.Timeout
        ):
            app = AppTest.from_file(str(ROOT / "page_4.py")).run()
            app.session_state.exchange_result = {"base": "USD", "quote": "KRW", "amount": 1, "rate": 1300, "date": "2026-10-30"}
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.error)
            self.assertEqual(len(app.metric), 0)

    def test_api_validation(self):
        with patch("exchange.requests.get") as get:
            get.return_value.json.return_value = {"rate": -1, "date": "2026-10-30"}
            with self.assertRaises(ValueError):
                get_rate("USD", "KRW")
            get.return_value.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()
