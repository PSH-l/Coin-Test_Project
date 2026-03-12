import streamlit as st
import requests

st.title("실시간 Bitcoin 가격")

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=krw"
data = requests.get(url).json()

price = data["bitcoin"]["krw"]

st.metric("Bitcoin", f"{price:,} KRW")
