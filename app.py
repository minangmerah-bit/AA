import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIG
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    layout="centered",
    page_icon="⚫"  # THE VOID
)

# =====================================================
# 2. UI STYLE (CLEAN & PROFESSIONAL)
# =====================================================
st.markdown("""
<style>
/* HIDE STREAMLIT DEFAULT UI */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}

/* FORCE BLACK BACKGROUND */
.stApp {
    background-color: #000000 !important;
}

/* LAYOUT CONTAINER */
.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* FONT GLOBAL */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    color: white;
}

/* --- INPUT FIELD STYLING (THE FIX) --- */
/* Menyembunyikan tombol +/- (Stepper) agar input bersih */
div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] {
    display: none !important;
}

/* Styling Kotak Input agar menyatu matte hitam */
div[data-baseweb="input"] {
    background-color: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: white !important;
    padding: 4px 0;
}
input {
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important; 
    font-size: 16px !important;
}

/* HEADER STYLE */
.title {
    font-size: 24px;
    font-weight: 700;
    color: white;
}
.subtitle {
    font-size: 11px;
    color: #8e8e8e;
}

/* SECTION LABELS */
.section {
    margin-top: 1.5rem;
    font-size: 10px;
    letter-spacing: 0.14em;
    color: #8e8e8e;
    text-transform: uppercase;
    font-weight: 700;
}

/* EXECUTION CARDS */
.exec {
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    border: 1px solid #222;
}

.buy { background: #102418; border-color: #143320; }
.sell { background: #2a1416; border-color: #3d1a1d; }

.exec-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* TEXT ELEMENTS INSIDE CARDS */
.asset { font-weight: 700; font-size: 15px; color: white; }
.price { font-size: 11px; color: #9a9a9a; margin-top: 2px; }
.action-sell { font-weight: 700; color: #ff6b6b; font-size: 13px; }
.value { font-weight: 700; font-size: 15px; color: white; }
.currency { font-size: 10px; color: #9a9a9a; text-align: right; }
.reason { font-size: 11px; color: #9a9a9a; margin-top: 4px; padding-top:4px; border-top: 1px solid rgba(255,255,255,0.05); }

/* BUTTON STYLE */
.stButton > button {
    width: 100%;
    background: white;
    color: black;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.7rem;
    border: none;
    margin-top: 10px;
}
.stButton > button:hover {
    background: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FX LOGIC (LOCKED & AUDITED)
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
# INPUT (VISUAL FIXED: NO BUTTONS)
# =====================================================
st.markdown("<div class='section'>CAPITAL CONFIG</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
# step=0.0 dan CSS di atas bekerja sama menghilangkan tombol +/-
budget = c1.number_input("Target", 300.0, step=0.0, label_visibility="collapsed")
used   = c2.number_input("Used", 0.0, step=0.0, label_visibility="collapsed")
extra  = c3.number_input("Extra", 0.0, step=0.0, label_visibility="collapsed")

c1.caption("Target ($)")
c2.caption("Used ($)")
c3.caption("Extra ($)")

total_dana_usd = (budget - used) + extra

st.markdown("<div class='section'>INVENTORY (ON = EMPTY)</div>", unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)
no_pltr = i1.toggle("PLTR", False)
no_qqq  = i1.toggle("QQQ", False)
no_btc  = i2.toggle("BTC", False)
no_gld  = i2.toggle("GLD", False)
no_mstr = i3.toggle("MSTR", False)

inv_data = {
    'PLTR': not no_pltr, 'BTC': not no_btc, 'MSTR': not no_mstr,
    'QQQ': not no_qqq, 'GLD': not no_gld
}

# =====================================================
# SIGNAL ENGINE (PETER PROTOCOL - LOCKED)
# =====================================================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    # Drawdown Logic
    cur_dd = (series - series.rolling(200, min_periods=1).max()).iloc[-1] / series.rolling(200, min_periods=1).max().iloc[-1]
    # RSI Logic
    rsi = 100 - (100 / (1 + (series.diff().where(lambda x:x>0,0).rolling(14).mean() /
                            (-series.diff().where(lambda x:x<0,0).rolling(14).mean()))))
    cur_rsi = rsi.iloc[-1]

    action, reason = "WAIT", "Stable"

    # STRATEGY RULES
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
        'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR',
        'QQQ':'QQQ', 'GLD':'GLD'
    }

    sell, buy = [], []

    with st.spinner("Processing..."):
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
            except: pass

    # OUTPUT: SELL
    if sell:
        st.markdown("<div class='section' style='color:#ff6b6b'>LIQUIDATION ORDER</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class="exec sell">
                <div class="exec-top">
                    <div>
                        <div class="asset">{x['sym']}</div>
                        <div class="price">${x['price']:,.2f}</div>
                    </div>
                    <div class="action-sell">SELL</div>
                </div>
                <div class="reason">{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

    # OUTPUT: BUY
    if buy:
        st.markdown("<div class='section' style='color:#4ade80'>ACQUISITION TARGETS</div>", unsafe_allow_html=True)

        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())

        for x in buy:
            sym = x['sym']
            if total_dana_usd>1 and total_w>0:
                usd = total_dana_usd * active[sym]/total_w
                if sym in ['BTC','GLD']:
                    val, cur = f"Rp {usd*kurs_rupiah:,.0f}", "IDR"
                else:
                    val, cur = f"${usd:,.2f}", "USD"
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
        st.info("System Stable. No Action Required.")
