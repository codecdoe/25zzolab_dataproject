import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Global Top 10 Stocks", layout="wide")

st.title("📈 글로벌 시가총액 Top 10 기업의 최근 1년 주가 변화")

# 글로벌 시가총액 Top 10 기업 (2025년 기준 추정)
companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 거래소
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

# 선택 필터
selected_companies = st.multiselect("📌 보고 싶은 기업을 선택하세요:", options=list(companies.keys()), default=list(companies.keys())[:5])

# 기간 설정: 최근 1년
end_date = datetime.today()
start_date = end_date - timedelta(days=365)


# 데이터 가져오기 + 유효성 검사 추가
st.info("💡 주가 데이터를 불러오는 데 시간이 조금 걸릴 수 있습니다.")
data = {}
for name in selected_companies:
    ticker = companies[name]
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # 데이터가 비어있지 않은 경우에만 추가
    if not stock_data.empty:
        data[name] = stock_data['Close']
    else:
        st.warning(f"⚠️ {name} ({ticker})의 데이터를 불러올 수 없습니다.")

# 데이터 유효성 확인
if data:
    df = pd.DataFrame(data)

    # Plotly 시각화
    fig = go.Figure()
    for company in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[company], mode='lines', name=company))

    fig.update_layout(
        title="최근 1년간 주가 변화 (종가 기준)",
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ 선택한 기업들의 주가 데이터를 가져올 수 없습니다.")

