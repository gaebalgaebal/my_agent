import requests
import streamlit as st

from exchange import get_currencies, get_rate


@st.cache_data(ttl=86400, show_spinner=False)
def currencies():
    return get_currencies()


@st.cache_data(ttl=3600, show_spinner=False)
def latest_rate(base, quote):
    return get_rate(base, quote)


st.title("💱 환율 조회")
st.caption("통화와 금액을 선택하면 최신 환율로 계산합니다.")

try:
    with st.spinner("통화 목록을 불러오는 중..."):
        available = currencies()
    codes = sorted(available)
except (requests.RequestException, ValueError, KeyError, TypeError):
    st.error("통화 목록을 불러오지 못했습니다. 네트워크를 확인하고 다시 시도하세요.")
    if st.button("다시 시도"):
        currencies.clear()
        st.rerun()
    st.stop()

with st.form("exchange_form"):
    left, right = st.columns(2)
    with left:
        base = st.selectbox(
            "기준 통화", codes, index=codes.index("USD") if "USD" in codes else 0,
            format_func=lambda code: f"{code} · {available[code]}",
        )
    with right:
        quote = st.selectbox(
            "대상 통화", codes, index=codes.index("KRW") if "KRW" in codes else 0,
            format_func=lambda code: f"{code} · {available[code]}",
        )
    amount = st.number_input("환산할 금액", min_value=0.0, max_value=1e12, value=1.0, step=1.0)
    submitted = st.form_submit_button("환율 조회", type="primary", width="stretch")

if submitted:
    # 조회 실패 시 이전 결과를 현재 입력의 결과처럼 표시하지 않습니다.
    st.session_state.pop("exchange_result", None)
    if base == quote:
        st.session_state.exchange_result = {
            "base": base, "quote": quote, "amount": amount, "rate": 1.0, "date": None
        }
    else:
        try:
            with st.spinner("최신 환율을 조회하는 중..."):
                result = latest_rate(base, quote)
            st.session_state.exchange_result = {
                "base": base, "quote": quote, "amount": amount, **result
            }
        except (requests.RequestException, ValueError, KeyError, TypeError):
            st.error("환율을 조회하지 못했습니다. 해당 통화 쌍의 제공 여부와 네트워크를 확인하고 다시 시도하세요.")

if "exchange_result" in st.session_state:
    result = st.session_state.exchange_result
    st.divider()
    st.subheader("환산 결과")
    st.metric(
        f"{result['amount']:,.2f} {result['base']} 환산 금액",
        f"{result['amount'] * result['rate']:,.2f} {result['quote']}",
    )
    st.write(f"1 {result['base']} = {result['rate']:,.6f} {result['quote']}")
    if result["date"]:
        st.caption(f"기준일 {result['date']}")
    else:
        st.caption("같은 통화의 환율은 1입니다.")

st.caption("일별 참고 환율이며, 은행의 실제 환전 수수료와 매매 환율은 반영하지 않습니다.")
st.markdown("출처: [Frankfurter](https://frankfurter.dev/)")
