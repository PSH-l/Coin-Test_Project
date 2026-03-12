import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 실시간 암호화폐 대시보드")

st.write("CoinGecko API 기반 실시간 코인 정보")

# API 주소
url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "krw",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": True
}

try:
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        st.error("API 요청 실패")
        st.stop()

    data = response.json()

    if not isinstance(data, list):
        st.error("API 데이터 형식 오류")
        st.write(data)
        st.stop()

    df = pd.DataFrame(data)

except Exception as e:
    st.error("데이터 가져오기 실패")
    st.write(e)
    st.stop()

# 필요한 컬럼
columns = [
    "name",
    "symbol",
    "image",
    "current_price",
    "price_change_percentage_24h",
    "total_volume",
    "sparkline_in_7d"
]

existing_columns = [c for c in columns if c in df.columns]

coins = df[existing_columns]

if coins.empty:
    st.warning("코인 데이터를 불러오지 못했습니다.")
    st.stop()

st.divider()

# 검색 기능
search = st.text_input("🔎 코인 검색")

if search:
    coins = coins[coins["name"].str.contains(search, case=False)]

# TOP 코인 카드
st.subheader("🔥 TOP 코인")

cols = st.columns(5)

for i, row in coins.head(5).iterrows():
    with cols[i]:

        if "image" in row:
            st.image(row["image"], width=50)

        price = row.get("current_price", 0)
        change = row.get("price_change_percentage_24h", 0)

        st.metric(
            label=row.get("name", "Unknown"),
            value=f"{price:,} KRW",
            delta=f"{change:.2f}%"
        )

st.divider()

# 코인 선택
st.subheader("📈 가격 그래프")

coin_names = coins["name"].tolist()

selected_coin = st.selectbox("코인 선택", coin_names)

coin_data = df[df["name"] == selected_coin]

if not coin_data.empty and "sparkline_in_7d" in coin_data.columns:

    spark_data = coin_data.iloc[0]["sparkline_in_7d"]["price"]

    chart_df = pd.DataFrame({
        "price": spark_data
    })

    st.line_chart(chart_df)

st.divider()

# 거래량 표시
st.subheader("💸 거래량")

volume_df = coins[["name", "total_volume"]]

volume_df.columns = ["Coin", "Volume"]

st.bar_chart(volume_df.set_index("Coin"))

st.divider()

# 가격 테이블
st.subheader("📊 코인 가격 테이블")

table_df = coins[[
    "name",
    "symbol",
    "current_price",
    "price_change_percentage_24h",
    "total_volume"
]]

table_df.columns = [
    "Coin",
    "Symbol",
    "Price (KRW)",
    "24h Change (%)",
    "Volume"
]

st.dataframe(table_df, use_container_width=True)

st.divider()

st.caption(
    f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

st.caption("데이터 출처: CoinGecko API")
