import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide"
)

# 배너 이미지
st.image(
    "https://images.unsplash.com/photo-1640161704729-cbe966a08476",
    use_container_width=True
)

st.title("💰 실시간 암호화폐 대시보드")

st.write("실시간 암호화폐 가격 정보 (CoinGecko API)")

# API 요청
url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "krw",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

data = requests.get(url, params=params).json()

df = pd.DataFrame(data)

# 필요한 컬럼만 선택
coins = df[[
    "name",
    "symbol",
    "image",
    "current_price",
    "price_change_percentage_24h"
]]

st.divider()

# 검색 기능
search = st.text_input("🔎 코인 검색")

if search:
    coins = coins[coins["name"].str.contains(search, case=False)]

# TOP10 코인 카드
st.subheader("🔥 TOP 코인")

cols = st.columns(5)

for i, row in coins.head(5).iterrows():
    with cols[i]:
        st.image(row["image"], width=50)
        st.metric(
            label=row["name"],
            value=f"{row['current_price']:,} KRW",
            delta=f"{row['price_change_percentage_24h']:.2f}%"
        )

cols2 = st.columns(5)

for i, row in coins.iloc[5:10].iterrows():
    with cols2[i]:
        st.image(row["image"], width=50)
        st.metric(
            label=row["name"],
            value=f"{row['current_price']:,} KRW",
            delta=f"{row['price_change_percentage_24h']:.2f}%"
        )

st.divider()

# 가격 테이블
st.subheader("📊 코인 가격 테이블")

table_df = coins[[
    "name",
    "symbol",
    "current_price",
    "price_change_percentage_24h"
]]

table_df.columns = [
    "Coin",
    "Symbol",
    "Price (KRW)",
    "24h Change (%)"
]

st.dataframe(table_df, use_container_width=True)

st.divider()

# 마지막 업데이트 시간
st.caption(
    f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

st.caption("데이터 출처: CoinGecko API")

# 자동 새로고침 (60초)
time.sleep(60)
st.rerun()
