import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="미국주식 vs 가상화폐 수익률 비교", layout="wide")

st.title("💵 미국 주식 vs 💰 가상화폐 수익률 비교 (DCA 기준)")

# 비교할 자산 목록
assets = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Ethereum (ETH-USD)": "ETH-USD"
}

selected_assets = st.multiselect("비교할 자산 선택:", list(assets.keys()), default=list(assets.keys()))

# 기간 선택
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 매월 투자금
monthly_investment = st.slider("매월 투자금 (USD)", 10, 1000, 100, step=10)

# 주가 및 가격 데이터 수집
st.info("📦 데이터를 불러오는 중입니다...")
data = {}
for name, ticker in assets.items():
    df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    if not df.empty:
        df = df.resample('M').last()  # 월별 마지막 날짜 기준
        data[name] = df['Close']
    else:
        st.warning(f"{name} 의 데이터를 가져오지 못했습니다.")

# 💹 수익률 계산 함수 (DCA 방식)
def simulate_dca(prices):
    prices = prices.dropna()
    prices = prices[prices > 0]

    total_invested = len(prices) * monthly_investment
    total_shares = (monthly_investment / prices).sum()
    final_value = total_shares * prices.iloc[-1]

    return {
        "투자원금": total_invested,
        "최종가치": round(final_value, 2),
        "수익률": round((final_value - total_invested) / total_invested * 100, 2)
    }

# 결과 계산
if data:
    results = {name: simulate_dca(prices) for name, prices in data.items()}
    df_result = pd.DataFrame(results).T
    df_result = df_result.rename(columns={"투자원금": "💸 투자원금", "최종가치": "📈 최종가치", "수익률": "📊 수익률 (%)"})

    st.subheader("📊 수익률 비교 표")
    st.dataframe(df_result)

    # 시각화
    fig = go.Figure()
    for name, prices in data.items():
        fig.add_trace(go.Scatter(x=prices.index, y=prices, mode="lines", name=name))

    fig.update_layout(
        title="자산별 가격 변화 (최근 1년)",
        xaxis_title="날짜",
        yaxis_title="가격 (USD)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ 데이터를 불러올 수 없습니다. 선택한 자산을 다시 확인해주세요.")
