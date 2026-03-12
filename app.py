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

st.write("CoinGecko API 기반 코인 정보")

# API 캐싱 (60초)
@st.cache_data(ttl=60)
def get_crypto_data():

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "krw",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": True
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return None

    return response.json()


data = get_crypto_data()

# API 실패 처리
if data is None:
    st.error("❌ API 요청 실패 (잠시 후 새로고침 해주세요)")
    st.stop()

df = pd.DataFrame(data)

if df.empty:
    st.warning("코인 데이터를 가져오지 못했습니다.")
    st.stop()

st.divider()

# 검색
search = st.text_input("🔎 코인 검색")

if search:
    df = df[df["name"].str.contains(search, case=False)]

# TOP 코인 카드
st.subheader("🔥 TOP 코인")

cols = st.columns(5)

for i, row in df.head(5).iterrows():

    with cols[i]:

        st.image(row["image"], width=50)

        st.metric(
            label=row["name"],
            value=f"{row['current_price']:,} KRW",
            delta=f"{row['price_change_percentage_24h']:.2f}%"
        )

st.divider()

# 코인 선택
st.subheader("📈 가격 그래프")

coin_names = df["name"].tolist()

selected_coin = st.selectbox(
    "그래프 확인 코인 선택",
    coin_names
)

coin_data = df[df["name"] == selected_coin]

if not coin_data.empty:

    spark = coin_data.iloc[0]["sparkline_in_7d"]["price"]

    chart_df = pd.DataFrame({
        "price": spark
    })

    st.line_chart(chart_df)

st.divider()

# 거래량 그래프
st.subheader("💸 거래량")

volume_df = df[["name", "total_volume"]]

volume_df.columns = ["Coin", "Volume"]

st.bar_chart(volume_df.set_index("Coin"))

st.divider()

# 가격 테이블
st.subheader("📊 코인 가격 테이블")

table_df = df[[
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
