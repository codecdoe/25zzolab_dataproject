import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("DCA 수익률 비교: SKYY vs Bitcoin (BTC)")

START_DATE = "2024-05-01"
END_DATE = "2025-05-01"

# 💰 하루 투자 금액 선택
invest_amount = st.slider("하루 투자 금액 (USD)", min_value=1, max_value=100, value=10, step=1)

# 데이터 다운로드
@st.cache_data
def get_price_data(ticker):
    df = yf.download(ticker, start=START_DATE, end=END_DATE)
    df = df[["Close"]].dropna()
    df.rename(columns={"Close": ticker}, inplace=True)
    return df

# 수익률 계산 함수 (💸 금액을 인자로 받음)
def simulate_dca(df: pd.DataFrame, daily_invest: float):
    df = df.copy()
    df["Investment"] = daily_invest
    df["Shares"] = df["Investment"] / df.iloc[:, 0]
    df["TotalShares"] = df["Shares"].cumsum()
    df["TotalInvested"] = df["Investment"].cumsum()
    df["PortfolioValue"] = df["TotalShares"] * df.iloc[:, 0]
    df["Profit"] = df["PortfolioValue"] - df["TotalInvested"]
    df["ReturnRate"] = df["Profit"] / df["TotalInvested"] * 100
    df["Date"] = df.index
    return df

# 가격 데이터 가져오기
skyy_data = get_price_data("SKYY")
btc_data = get_price_data("BTC-USD")

# 날짜 정렬
common_dates = skyy_data.index.intersection(btc_data.index)
skyy_data = skyy_data.loc[common_dates]
btc_data = btc_data.loc[common_dates]

# 수익률 계산 (💸 선택한 투자금액 사용)
skyy_result = simulate_dca(skyy_data, invest_amount)
btc_result = simulate_dca(btc_data, invest_amount)

# Plotly 그래프
fig = go.Figure()
fig.add_trace(go.Scatter(x=skyy_result["Date"], y=skyy_result["ReturnRate"],
                         mode="lines", name="SKYY 수익률"))
fig.add_trace(go.Scatter(x=btc_result["Date"], y=btc_result["ReturnRate"],
                         mode="lines", name="Bitcoin 수익률"))

fig.update_layout(
    title=f"{START_DATE} ~ {END_DATE} 적립식 투자 수익률 비교 (하루 ${invest_amount})",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    legend_title="자산",
    hovermode="x unified"
)

st.plotly_chart(fig)

# 📊 요약 표
st.subheader("누적 투자 및 평가 금액 비교")
summary = pd.DataFrame({
    "종목": ["SKYY", "BTC"],
    "총 투자금 ($)": [
        round(skyy_result["TotalInvested"].iloc[-1], 2),
        round(btc_result["TotalInvested"].iloc[-1], 2),
    ],
    "현재 평가금액 ($)": [
        round(skyy_result["PortfolioValue"].iloc[-1], 2),
        round(btc_result["PortfolioValue"].iloc[-1], 2),
    ],
    "총 수익률 (%)": [
        round(skyy_result["ReturnRate"].iloc[-1], 2),
        round(btc_result["ReturnRate"].iloc[-1], 2),
    ]
})
st.dataframe(summary)

'''
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.title("DCA 수익률 비교: SKYY vs Bitcoin (BTC)")

START_DATE = "2024-05-01"
END_DATE = "2025-05-01"
INVEST_AMOUNT = 10  # 하루 투자 금액

# 다운로드
@st.cache_data
def get_price_data(ticker):
    df = yf.download(ticker, start=START_DATE, end=END_DATE)
    df = df[["Close"]].dropna()
    df.rename(columns={"Close": ticker}, inplace=True)
    return df

def simulate_dca(df: pd.DataFrame):
    df = df.copy()
    df["Investment"] = INVEST_AMOUNT
    df["Shares"] = df["Investment"] / df.iloc[:, 0]  # 첫 번째 컬럼이 가격
    df["TotalShares"] = df["Shares"].cumsum()
    df["TotalInvested"] = df["Investment"].cumsum()
    df["PortfolioValue"] = df["TotalShares"] * df.iloc[:, 0]
    df["Profit"] = df["PortfolioValue"] - df["TotalInvested"]
    df["ReturnRate"] = df["Profit"] / df["TotalInvested"] * 100
    df["Date"] = df.index
    return df



# 데이터 수집
skyy_data = get_price_data("SKYY")
btc_data = get_price_data("BTC-USD")

# 공통 날짜로 정렬
common_dates = skyy_data.index.intersection(btc_data.index)
skyy_data = skyy_data.loc[common_dates]
btc_data = btc_data.loc[common_dates]

# 수익률 계산
skyy_result = simulate_dca(skyy_data["SKYY"])
btc_result = simulate_dca(btc_data["BTC-USD"])

# Plotly 시각화
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=skyy_result["Date"], y=skyy_result["ReturnRate"],
    mode="lines", name="SKYY 수익률"
))

fig.add_trace(go.Scatter(
    x=btc_result["Date"], y=btc_result["ReturnRate"],
    mode="lines", name="Bitcoin 수익률"
))

fig.update_layout(
    title="2024-05-01 ~ 2025-05-01 적립식 투자 수익률 비교 (매일 $10)",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    legend_title="자산",
    hovermode="x unified"
)

st.plotly_chart(fig)

# 선택: 누적 투자금, 현재 평가금액도 출력
st.subheader("누적 투자 및 평가 금액 비교")
summary = pd.DataFrame({
    "종목": ["SKYY", "BTC"],
    "총 투자금 ($)": [
        round(skyy_result["TotalInvested"].iloc[-1], 2),
        round(btc_result["TotalInvested"].iloc[-1], 2),
    ],
    "현재 평가금액 ($)": [
        round(skyy_result["PortfolioValue"].iloc[-1], 2),
        round(btc_result["PortfolioValue"].iloc[-1], 2),
    ],
    "총 수익률 (%)": [
        round(skyy_result["ReturnRate"].iloc[-1], 2),
        round(btc_result["ReturnRate"].iloc[-1], 2),
    ]
})
st.dataframe(summary)
'''
