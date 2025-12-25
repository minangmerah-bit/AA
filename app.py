import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIG
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. UI STYLE (ENTERPRISE GRADE - SEAMLESS INPUT)
# =====================================================
st.markdown("""
<style>
/* --- HIDE DEFAULT MENUS --- */
#MainMenu, header, footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}

/* --- FORCE PITCH BLACK BACKGROUND --- */
.stApp {
    background-color: #000000 !important;
}

/* --- LAYOUT ADJUSTMENT --- */
.block-container {
    max-width: 600px; /* Lebih ramping agar pas di HP */
    padding-top: 2rem;
    padding-bottom: 2rem;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    color: white;
}

/* --- HEADER TYPOGRAPHY --- */
.title {
    font-size: 26px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.5px;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 11px;
    color: #666;
    margin-top: 4px;
    font-family: monospace;
    letter-spacing: 1px;
}

/* --- SECTION LABELS --- */
.section {
    margin-top: 25px;
    margin-bottom: 8px;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #555;
    text-transform: uppercase;
    font-weight: 700;
}

/* --- INPUT FIELDS (THE FIX: SEAMLESS BOX) --- */
/* Menghilangkan tombol +/- (Stepper) agar input jadi kotak utuh */
button[kind="secondaryFormSubmit"] {display: none;}
div[data-testid="stNumberInputStepDown"] {display: none !important;}
div[data-testid="stNumberInputStepUp"] {display: none !important;}

/* Styling Kotak Input */
div[data-baseweb="input"] {
    background-color: #111 !important; /* Abu sangat gelap */
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: white !important;
    padding: 5px; /* Padding biar angka tidak mepet */
}
input {
    color: white !important;
    font-weight: 600 !important;
    font-size: 16px !important; /* Angka lebih besar/jelas */
    text-align: center !important; /* Angka di tengah (Opsional, lebih rapi) */
}

/* --- EXECUTION CARDS --- */
.exec {
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    border: 1px solid #222;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.buy { background: #0a1f10; border-color: #143320; }
.sell { background: #260d0f; border-color: #3d1a1d; }

.asset-box {
    display: flex;
    flex-direction: column;
}
.asset-name { font-weight: 700; font-size: 16px; color: white; }
.asset-price { font-size: 11px; color: #777; margin-top: 2px; }

.result-box {
    text-align: right;
}
.action-sell { font-weight: 800; color: #ff5252; font-size: 14px; letter-spacing: 0.5px; }
.value-buy { font-weight: 700; font-size: 16px; color: white; }
.currency { font-size: 10px; color: #666; }
.reason { font-size: 10px; color: #666; margin-top: 4px; text-transform: uppercase; }

/* --- BUTTON --- */
.stButton > button {
    width: 100%;
    background-color: white;
    color: black;
    font-weight: 800;
    border-radius: 8px;
    padding: 14px 0;
    font-size: 14px;
    border: none;
    margin-top: 15px;
    transition: 0.2s;
}
.stButton > button:hover {
    background-color: #cccccc;
    transform: scale(0.99);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (PETER PROTOCOL - LOCKED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try:
        return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except:
        return 16000.0

kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER UI
# =====================================================
c_head, c_rate = st.columns([3,1])
with c_head:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>ARCHITECT: PETER</div>", unsafe_allow_html=True)
with c_rate:
    st.markdown(
        f"<div style='text-align:right;font-size:10px;color:#555;padding-top:10px;font-family:monospace'>IDR {kurs_rupiah:,.0f}</div>",
        unsafe_allow_html=True
    )

# =====================================================
# 5. INPUTS (SEAMLESS SINGLE BOX)
# =====================================================
st.markdown("<div class='section'>CAPITAL ALLOCATION</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
# Input tanpa tombol +/- (Berkat CSS di atas)
budget = c1.number_input("T", 300.0, step=0.0, label_visibility="collapsed")
used   = c2.number_input("U", 0.0, step=0.0, label_visibility="collapsed")
extra  = c3.number_input("E", 0.0, step=0.0, label_visibility="collapsed")

# Label minimalis di bawah
c1.caption("Target ($)")
c2.caption("Used ($)")
c3.caption("Extra ($)")

total_dana_usd = (budget - used) + extra

st.markdown("<div class='section'>INVENTORY STATUS (ON = EMPTY)</div>", unsafe_allow_html=True)
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
# 6. ENGINE (LOGIC INTACT)
# =====================================================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    # Drawdown logic
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
# 7. EXECUTION
# =====================================================
st.write("")
if st.button("RUN DIAGNOSTIC", use_container_width=True):

    tickers = {
        'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR',
        'QQQ':'QQQ', 'GLD':'GLD'
    }

    sell, buy = [], []

    with st.spinner("Analyzing..."):
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

    # --- OUTPUT DISPLAY (CLEAN CARDS) ---
    st.write("")
    
    if sell:
        st.markdown("<div class='section' style='color:#ff5252'>LIQUIDATION ORDER</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class="exec sell">
                <div class="asset-box">
                    <div class="asset-name">{x['sym']}</div>
                    <div class="asset-price">${x['price']:,.2f}</div>
                    <div class="reason" style="color:#ff5252">{x['reason']}</div>
                </div>
                <div class="result-box">
                    <div class="action-sell">SELL</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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
                <div class="asset-box">
                    <div class="asset-name">{sym}</div>
                    <div class="asset-price">${x['price']:,.2f}</div>
                    <div class="reason">{x['reason']}</div>
                </div>
                <div class="result-box">
                    <div class="value-buy">{val}</div>
                    <div class="currency">{cur}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy:
        st.info("Market is Neutral. No Action Required.")
