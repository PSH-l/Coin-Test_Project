import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Price Dashboard", page_icon="💰")

st.title("💰 실시간 코인 가격 대시보드")

st.write("CoinGecko API 기반 실시간 코인 가격")

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "krw",
    "include_24hr_change": "true"
}

data = requests.get(url, params=params).json()

coins = {
    "Bitcoin": data["bitcoin"]["krw"],
    "Ethereum": data["ethereum"]["krw"],
    "Solana": data["solana"]["krw"]
}

change = {
    "Bitcoin": data["bitcoin"]["krw_24h_change"],
    "Ethereum": data["ethereum"]["krw_24h_change"],
    "Solana": data["solana"]["krw_24h_change"]
}

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Bitcoin",
        value=f"{coins['Bitcoin']:,} KRW",
        delta=f"{change['Bitcoin']:.2f}%"
    )

with col2:
    st.metric(
        label="Ethereum",
        value=f"{coins['Ethereum']:,} KRW",
        delta=f"{change['Ethereum']:.2f}%"
    )

with col3:
    st.metric(
        label="Solana",
        value=f"{coins['Solana']:,} KRW",
        delta=f"{change['Solana']:.2f}%"
    )

st.divider()

st.subheader("📊 코인 가격 테이블")

df = pd.DataFrame({
    "Coin": coins.keys(),
    "Price (KRW)": coins.values(),
    "24h Change (%)": change.values()
})

st.dataframe(df)

st.divider()

st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.caption("데이터 출처: CoinGecko API")
