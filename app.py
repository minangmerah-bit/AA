import streamlit as st
import yfinance as yf

# =====================================================
# SYSTEM CONFIG
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    layout="centered"
)

# =====================================================
# MOBILE-FIRST UI STYLE
# =====================================================
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

/* Header */
.title {
    font-size: 24px;
    font-weight: 700;
}
.subtitle {
    font-size: 11px;
    color: #8e8e8e;
}

/* Section */
.section {
    margin-top: 1.2rem;
    font-size: 10px;
    letter-spacing: 0.14em;
    color: #8e8e8e;
}

/* Execution item */
.exec {
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 6px;
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

.price {
    font-size: 11px;
    color: #9a9a9a;
    margin-top: 2px;
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

.reason {
    font-size: 11px;
    color: #9a9a9a;
    margin-top: 2px;
}

/* Button */
.stButton > button {
    background: white;
    color: black;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FX LOGIC (UNCHANGED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try:
        return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except:
        return 16000.0

kurs_rupiah = get_usd_idr()

# =====================================================
# HEADER
# =====================================================
l, r = st.columns([3,1])
with l:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Architect: Peter</div>", unsafe_allow_html=True)
with r:
    st.markdown(
        f"<div style='text-align:right;font-size:11px;color:#8e8e8e;padding-top:10px'>IDR {kurs_rupiah:,.0f}</div>",
        unsafe_allow_html=True
    )

# =====================================================
# INPUT
# =====================================================
st.markdown("<div class='section'>CAPITAL</div>", unsafe_allow_html=True)
budget = st.number_input("Target", 300.0, step=10.0)
used   = st.number_input("Used", 0.0, step=10.0)
extra  = st.number_input("Extra", 0.0, step=10.0)

total_dana_usd = (budget - used) + extra

st.markdown("<div class='section'>INVENTORY (ON = EMPTY)</div>", unsafe_allow_html=True)
no_pltr = st.toggle("PLTR", False)
no_qqq  = st.toggle("QQQ", False)
no_btc  = st.toggle("BTC", False)
no_gld  = st.toggle("GLD", False)
no_mstr = st.toggle("MSTR", False)

inv_data = {
    'PLTR': not no_pltr,
    'BTC': not no_btc,
    'MSTR': not no_mstr,
    'QQQ': not no_qqq,
    'GLD': not no_gld
}

# =====================================================
# SIGNAL ENGINE (IDENTICAL)
# =====================================================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    cur_dd = (series - series.rolling(200, min_periods=1).max()).iloc[-1] / series.rolling(200, min_periods=1).max().iloc[-1]
    rsi = 100 - (100 / (1 + (series.diff().where(lambda x:x>0,0).rolling(14).mean() /
                            (-series.diff().where(lambda x:x<0,0).rolling(14).mean()))))
    cur_rsi = rsi.iloc[-1]

    action, reason = "WAIT", "Stable"

    if cur_rsi > 80 or (price - sma200)/sma200 > 0.6:
        action, reason = "SELL", f"Overheat RSI {cur_rsi:.0f}"
    elif price > sma200:
        action, reason = "BUY", "Uptrend"
    elif (symbol=='PLTR' and cur_dd<-0.30) or (symbol in ['BTC','MSTR'] and cur_dd<-0.20):
        action, reason = "BUY", f"Dip {cur_dd*100:.0f}%"

    return price, reason, action

# =====================================================
# EXECUTION
# =====================================================
st.write("")
if st.button("RUN DIAGNOSTIC", use_container_width=True):

    tickers = {
        'PLTR':'PLTR',
        'BTC-USD':'BTC',
        'MSTR':'MSTR',
        'QQQ':'QQQ',
        'GLD':'GLD'
    }

    sell, buy = [], []

    for sym, key in tickers.items():
        try:
            df = yf.download(sym, period="300d", interval="1d", progress=False)
            if df.empty: continue

            px = df['Close'] if isinstance(df.columns,str) else df.xs('Close',axis=1,level=0).iloc[:,0]
            price, reason, action = get_signal(px, key)

            item = {'sym': key, 'price': price, 'reason': reason}
            if action=="SELL" and inv_data.get(key,True):
                sell.append(item)
            elif action=="BUY":
                buy.append(item)
        except:
            pass

    if sell:
        st.markdown("<div class='section'>SELL</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class="exec sell">
                <div class="asset">{x['sym']}</div>
                <div class="price">${x['price']:,.2f}</div>
                <div class="action-sell">SELL</div>
                <div class="reason">{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    if buy:
        st.markdown("<div class='section'>BUY</div>", unsafe_allow_html=True)

        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())

        for x in buy:
            sym = x['sym']
            if total_dana_usd>1 and total_w>0:
                usd = total_dana_usd * active[sym]/total_w
                if sym in ['BTC','GLD']:
                    val = f"Rp {usd*kurs_rupiah:,.0f}"
                    cur = "IDR"
                else:
                    val = f"${usd:,.2f}"
                    cur = "USD"
            else:
                val,cur="HOLD","-"

            st.markdown(f"""
            <div class="exec buy">
                <div class="exec-top">
                    <div>
                        <div class="asset">{sym}</div>
                        <div class="price">${x['price']:,.2f}</div>
                    </div>
                    <div>
                        <div class="value">{val}</div>
                        <div class="currency">{cur}</div>
                    </div>
                </div>
                <div class="reason">{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy:
        st.info("No action required.")
