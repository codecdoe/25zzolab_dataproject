import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="DCA 수익률 비교: SKYY vs BTC", layout="wide")

st.title("💸 하루에 10달러씩 분할매수: SKYY vs Bitcoin")

# 날짜 범위: 최근 1년
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 자산 티커
assets = {
    'SKYY': 'SKYY',
    'Bitcoin (BTC-USD)': 'BTC-USD'
}

# 데이터 수집
@st.cache_data
def get_price_data(ticker):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df['Close']

data = {name: get_price_data(ticker) for name, ticker in assets.items()}

# 분할매수 시뮬레이션 함수
def simulate_dca(price_series, daily_investment=10):
    investment_dates = price_series.index
    total_units = 0
    total_invested = 0
    portfolio_value = []

    for date in investment_dates:
        price = price_series.loc[date]
        if price > 0:
            units = daily_investment / price
            total_units += units
            total_invested += daily_investment
        current_value = total_units * price
        return_rate = (current_value - total_invested) / total_invested
        portfolio_value.append({
            'Date': date,
            'Invested': total_invested,
            'Value': current_value,
            'Return': return_rate
        })

    return pd.DataFrame(portfolio_value).set_index('Date')

# DCA 결과 계산
results = {name: simulate_dca(prices) for name, prices in data.items()}

# Plotly 시각화
fig = go.Figure()
for name, df in results.items():
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Return'] * 100,
        mode='lines',
        name=name
    ))

fig.update_layout(
    title="📊 분할매수 수익률 비교 (지난 1년, 매일 $10 투자)",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 수익률 요약
st.subheader("📈 누적 투자 요약")
summary_data = {
    name: {
        '총 투자금 ($)': f"{df['Invested'].iloc[-1]:,.2f}",
        '최종 평가금액 ($)': f"{df['Value'].iloc[-1]:,.2f}",
        '총 수익률 (%)': f"{df['Return'].iloc[-1] * 100:.2f}"
    }
    for name, df in results.items()
}
st.dataframe(pd.DataFrame(summary_data).T)
