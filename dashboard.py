import streamlit as st
import pandas as pd
import time
from analysis import (
    top_5_gainers,
    top_5_market_cap,
    average_market_cap,
    total_market_value,
    volatility_ranking
)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Crypto Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- AUTO REFRESH ---------------- #
REFRESH_INTERVAL = 60  # seconds

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.rerun()

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .kpi-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
    }
    .kpi-label {
        font-size: 14px;
        color: #AAAAAA;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Overview", "Market Analysis", "Volatility Ranking"]
)

st.sidebar.markdown("---")
st.sidebar.info("Data updates every 60 seconds")

# ---------------- DATA FETCH ---------------- #
total_cap = total_market_value()[0][0]
avg_cap = average_market_cap()[0][0]
top_gainer = top_5_gainers()[0]
most_volatile = volatility_ranking()[0]

# ---------------- OVERVIEW PAGE ---------------- #
if page == "Overview":

    st.title("🚀 Real-Time Crypto Analytics Dashboard")
    st.markdown("Live market insights powered by CoinGecko API")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Market Cap</div>
                <div class="kpi-value">${total_cap:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Average Market Cap</div>
                <div class="kpi-value">${avg_cap:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Highest Gainer</div>
                <div class="kpi-value">{top_gainer[0]}<br>{top_gainer[1]:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Most Volatile</div>
                <div class="kpi-value">{most_volatile[0]}</div>
            </div>
        """, unsafe_allow_html=True)

# ---------------- MARKET ANALYSIS ---------------- #
elif page == "Market Analysis":

    st.header("📊 Top 5 Gainers vs Market Cap")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Top 5 Gainers")
        gainers_df = pd.DataFrame(
            top_5_gainers(),
            columns=["Coin", "24h Change"]
        )
        st.bar_chart(gainers_df.set_index("Coin"))

    with col2:
        st.subheader("🏆 Top 5 Market Cap")
        market_df = pd.DataFrame(
            top_5_market_cap(),
            columns=["Coin", "Market Cap"]
        )
        st.bar_chart(market_df.set_index("Coin"))

# ---------------- VOLATILITY PAGE ---------------- #
elif page == "Volatility Ranking":

    st.header("🔥 Volatility Ranking")

    vol_df = pd.DataFrame(
        volatility_ranking(),
        columns=["Coin", "Volatility"]
    )

    st.bar_chart(vol_df.set_index("Coin"))

    with st.expander("📄 View Raw Volatility Data"):
        st.dataframe(vol_df, use_container_width=True)