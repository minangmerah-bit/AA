import streamlit as st
import yfinance as yf
import pandas as pd

# =====================================================
# EXECUTOR X1 v1.0 — LOCKED
# Strategy: Rule-based | 1D Close | Manual Execution
# =====================================================

st.set_page_config(
    page_title="Executor X1",
    layout="centered"
)

# ===================== STYLE =========================
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.block-container {
    max-width: 680px;
    padding-top: 1.6rem;
    padding-bottom: 2rem;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
}

.title {
    font-size: 24px;
    font-weight: 700;
}

.subtitle {
    font-size: 11px;
    color: #8e8e8e;
}

.section {
    margin-top: 1.2rem;
    font-size: 10px;
    letter-spacing: 0.14em;
    color: #8e8e8e;
}

.exec {
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 8px;
}

.buy { background: #102418; }
.sell { background: #2a1416; }
.wait { background: #161618; }

.exec-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.asset {
    font-weight: 600;
    font-size: 14px;
}

.action-sell {
    font-weight: 700;
    color: #ff6b6b;
    font-size: 13px;
}

.value {
    font-weight: 700;
    font-size: 15px;
}

.currency {
    font-size: 10px;
    color: #9a9a9a;
    text-align: right;
}

.price {
    font-size: 10px;
    color: #6f6f6f;
    margin-top: 2px;
}

.reason {
    font-size: 11px;
    color: #9a9a9a;
    margin-top: 4px;
}

.stButton > button {
    background: white;
    color: black;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.7rem;
}
</style>
""", unsafe_allow_html=True)

# ===================== FX =============================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try:
        return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except:
        return 16000.0

kurs = get_usd_idr()

# ===================== HEADER =========================
l, r = st.columns([3,1])
with l:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>v1.0 • Strategy Locked</div>", unsafe_allow_html=True)
with r:
    st.markdown(
        f"<div style='text-align:right;font-size:11px;color:#8e8e8e;padding-top:10px'>IDR {kurs:,.0f}</div>",
        unsafe_allow_html=True
    )

# ===================== INPUT ==========================
st.markdown("<div class='section'>CAPITAL</div>", unsafe_allow_html=True)
budget = st.number_input("Target", 300.0, step=10.0)
used   = st.number_input("Used", 0.0, step=10.0)
extra  = st.number_input("Extra", 0.0, step=10.0)

available_usd = (budget - used) + extra

st.markdown("<div class='section'>INVENTORY (ON = EMPTY)</div>", unsafe_allow_html=True)
no_pltr = st.toggle("PLTR", False)
no_btc  = st.toggle("BTC", False)
no_mstr = st.toggle("MSTR", False)
no_qqq  = st.toggle("QQQ", False)
no_gld  = st.toggle("GLD", False)

inventory = {
    'PLTR': not no_pltr,
    'BTC': not no_btc,
    'MSTR': not no_mstr,
    'QQQ': not no_qqq,
    'GLD': not no_gld
}

# ===================== SIGNAL ENGINE ==================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    peak = series.rolling(200, min_periods=1).max().iloc[-1]
    dd = price / peak - 1

    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rsi = 100 - (100 / (1 + gain / loss))
    cur_rsi = rsi.iloc[-1]

    action = "WAIT"
    reason = "Stable"

    if cur_rsi > 80 or (price - sma200) / sma200 > 0.6:
        action, reason = "SELL", f"Overheat (RSI {cur_rsi:.0f})"
    elif price > sma200:
        action, reason = "BUY", "Uptrend"
    elif (symbol == "PLTR" and dd < -0.30) or (symbol in ["BTC","MSTR"] and dd < -0.20):
        action, reason = "BUY", f"Deep dip {dd*100:.0f}%"

    return price, action, reason

# ===================== RUN =============================
if st.button("RUN DIAGNOSTIC", use_container_width=True):

    tickers = {
        'PLTR': 'PLTR',
        'BTC': 'BTC-USD',
        'MSTR': 'MSTR',
        'QQQ': 'QQQ',
        'GLD': 'GLD'
    }

    sell, buy = [], []

    for name, tkr in tickers.items():
        df = yf.download(tkr, period="300d", interval="1d", progress=False)
        if df.empty:
            continue

        px = df['Close']
        price, action, reason = get_signal(px, name)

        item = {"sym": name, "price": price, "reason": reason}

        if action == "SELL" and inventory.get(name, True):
            sell.append(item)
        elif action == "BUY":
            buy.append(item)

    if sell:
        st.markdown("<div class='section'>SELL</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class="exec sell">
                <div class="exec-top">
                    <div class="asset">{x['sym']}</div>
                    <div class="action-sell">SELL</div>
                </div>
                <div class="price">${x['price']:.2f}</div>
                <div class="reason">{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    if buy:
        st.markdown("<div class='section'>BUY</div>", unsafe_allow_html=True)
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        total_w = sum(base_w[x['sym']] for x in buy)

        for x in buy:
            w = base_w[x['sym']] / total_w
            usd = available_usd * w
            val = f"${usd:,.2f}" if x['sym'] not in ['BTC','GLD'] else f"Rp {usd*kurs:,.0f}"

            st.markdown(f"""
            <div class="exec buy">
                <div class="exec-top">
                    <div class="asset">{x['sym']}</div>
                    <div>
                        <div class="value">{val}</div>
                    </div>
                </div>
                <div class="price">${x['price']:.2f}</div>
                <div class="reason">{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy:
        st.info("No action required.")
