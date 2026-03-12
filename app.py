import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Crypto Dashboard", page_icon="💰", layout="wide")

# 금융사이트 느낌 배너
st.image(
    "https://images.unsplash.com/photo-1640161704729-cbe966a08476",
    use_container_width=True
)

st.title("💰 실시간 코인 가격 대시보드")

st.write("CoinGecko API 기반 실시간 암호화폐 가격")

# API 호출
url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "krw",
    "include_24hr_change": "true"
}

data = requests.get(url, params=params).json()

# 가격 데이터
btc_price = data["bitcoin"]["krw"]
eth_price = data["ethereum"]["krw"]
sol_price = data["solana"]["krw"]

btc_change = data["bitcoin"]["krw_24h_change"]
eth_change = data["ethereum"]["krw_24h_change"]
sol_change = data["solana"]["krw_24h_change"]

st.divider()

# 코인 카드 UI
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://cryptologos.cc/logos/bitcoin-btc-logo.png", width=80)
    st.metric(
        label="Bitcoin",
        value=f"{btc_price:,} KRW",
        delta=f"{btc_change:.2f}%"
    )

with col2:
    st.image("https://cryptologos.cc/logos/ethereum-eth-logo.png", width=80)
    st.metric(
        label="Ethereum",
        value=f"{eth_price:,} KRW",
        delta=f"{eth_change:.2f}%"
    )

with col3:
    st.image("https://cryptologos.cc/logos/solana-sol-logo.png", width=80)
    st.metric(
        label="Solana",
        value=f"{sol_price:,} KRW",
        delta=f"{sol_change:.2f}%"
    )

st.divider()

# 가격 테이블
st.subheader("📊 코인 가격 테이블")

df = pd.DataFrame({
    "Coin": ["Bitcoin", "Ethereum", "Solana"],
    "Price (KRW)": [btc_price, eth_price, sol_price],
    "24h Change (%)": [btc_change, eth_change, sol_change]
})

st.dataframe(df, use_container_width=True)

st.divider()

# 마지막 업데이트
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("데이터 출처: CoinGecko API")
