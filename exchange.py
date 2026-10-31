"""Frankfurter 공개 API 조회. API 키는 필요하지 않습니다."""

import math

import requests

API_URL = "https://api.frankfurter.dev/v2"


def get_currencies():
    response = requests.get(f"{API_URL}/currencies", timeout=15)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or not data:
        raise ValueError("통화 목록이 비어 있습니다.")
    return {item["iso_code"]: item["name"] for item in data}


def get_rate(base, quote):
    response = requests.get(f"{API_URL}/rate/{base}/{quote}", timeout=15)
    response.raise_for_status()
    data = response.json()
    rate = float(data["rate"])
    if not math.isfinite(rate) or rate <= 0 or not data["date"]:
        raise ValueError("올바른 환율 데이터가 아닙니다.")
    return {"date": data["date"], "rate": rate}
