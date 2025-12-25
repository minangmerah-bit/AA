import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    layout="centered"
)

# =====================================================
# 2. UI ARCHITECTURE (MATTE BLACK & PRECISION LAYOUT)
# =====================================================
st.markdown("""
<style>
/* --- CORE CLEANUP --- */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}
.stApp { background-color: #000000 !important; }

/* --- CONTAINER --- */
.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* --- TYPOGRAPHY --- */
body { font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; color: white; }

/* --- INPUT ENGINEERING (NO BUTTONS, LEFT LABELS) --- */
/* 1. Hide Stepper Buttons (+/-) */
div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] {
    display: none !important;
}

/* 2. Input Box Styling */
div[data-baseweb="input"] {
    background-color: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 8px 0;
}

/* 3. Input Text (Center Aligned Number) */
input {
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important;
    font-size: 18px !important;
}

/* 4. Input Labels (Left Aligned) */
.input-label {
    font-size: 11px;
    color: #888;
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    text-align: left;
    padding-left: 2px;
}

/* --- HEADER & SECTIONS --- */
.title { font-size: 24px; font-weight: 700; color: white; letter-spacing: -0.5px; }
.subtitle {
    font-size: 12px; color: #666;
    font-family: "SF Mono", "Roboto Mono", monospace;
    margin-top: 4px;
}
.section {
    margin-top: 2.5rem;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #555;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 15px;
}

/* --- INTELLIGENT CARDS (THE FIX) --- */
.exec {
    background-color: #0a0a0a;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 16px; /* Padding lebih lega */
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.buy { border-left: 4px solid #2ecc71; }
.sell { border-left: 4px solid #e74c3c; }

/* Card Typography */
.asset-name { font-weight: 800; font-size: 17px; color: white; margin-bottom: 2px; }
.market-price { font-size: 13px; color: #eee; font-weight: 600; font-family: monospace; } /* Harga Pasar Jelas */
.asset-reason { font-size: 10px; color: #666; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px;}

.val-box { text-align: right; }
.val-main { font-weight: 800; font-size: 16px; color: white; }
.val-sub { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; margin-top: 2px;}

.tag-buy { color: #2ecc71; }
.tag-sell { color: #e74c3c; }

/* --- BUTTON --- */
.stButton > button {
    width: 100%;
    background: white;
    color: black;
    font-weight: 800;
    border-radius: 8px;
    padding: 14px 0;
    font-size: 14px;
    border: none;
    margin-top: 30px;
}
.stButton > button:hover { background: #cccccc; transform: scale(0.99); }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (PETER PROTOCOL - LOCKED & AUDITED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try: return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except: return 16000.0
kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER
# =====================================================
l, r = st.columns([3,1])
with l:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>rizqynandaputra</div>", unsafe_allow_html=True)
with r:
    st.markdown(f"<div style='text-align:right;font-size:11px;color:#555;padding-top:10px;font-family:monospace'>IDR {kurs_rupiah:,.0f}</div>", unsafe_allow_html=True)

# =====================================================
# 5. INPUT CONFIGURATION
# =====================================================
st.markdown("<div class='section'>CAPITAL CONFIGURATION</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='input-label'>TARGET ($)</div>", unsafe_allow_html=True)
    budget = st.number_input("Target", 300.0, step=1.0, label_visibility="collapsed")
with c2:
    st.markdown("<div class='input-label'>USED ($)</div>", unsafe_allow_html=True)
    used = st.number_input("Used", 0.0, step=1.0, label_visibility="collapsed")
with c3:
    st.markdown("<div class='input-label'>EXTRA ($)</div>", unsafe_allow_html=True)
    extra = st.number_input("Extra", 0.0, step=1.0, label_visibility="collapsed")

total_dana_usd = (budget - used) + extra

st.markdown("<div class='section'>INVENTORY STATUS (ON = EMPTY)</div>", unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)
no_pltr = i1.toggle("PLTR", False); no_qqq = i1.toggle("QQQ", False)
no_btc = i2.toggle("BTC", False); no_gld = i2.toggle("GLD", False)
no_mstr = i3.toggle("MSTR", False)
inv_data = {'PLTR': not no_pltr, 'BTC': not no_btc, 'MSTR': not no_mstr, 'QQQ': not no_qqq, 'GLD': not no_gld}

# =====================================================
# 6. ALGORITHM ENGINE (CORE)
# =====================================================
def get_signal(series, symbol):
    # 1. DATA EXTRACTION
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    
    # 2. DRAWDOWN LOGIC
    rolling_max = series.rolling(200, min_periods=1).max()
    cur_dd = (series - rolling_max).iloc[-1] / rolling_max.iloc[-1]
    
    # 3. RSI LOGIC (14)
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    cur_rsi = rsi.iloc[-1]

    action, reason = "WAIT", "Stable"

    # 4. DECISION HIERARCHY
    if cur_rsi > 80 or (price - sma200)/sma200 > 0.6: 
        action, reason = "SELL", f"Overheat RSI {cur_rsi:.0f}"
    elif price > sma200: 
        action, reason = "BUY", "Uptrend"
    elif (symbol=='PLTR' and cur_dd < -0.30) or (symbol in ['BTC','MSTR'] and cur_dd < -0.20): 
        action, reason = "BUY", f"Dip {cur_dd*100:.0f}%"

    return price, reason, action

# =====================================================
# 7. EXECUTION & RENDERING
# =====================================================
st.write("")
if st.button("RUN DIAGNOSTIC", use_container_width=True):
    tickers = {'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR', 'QQQ':'QQQ', 'GLD':'GLD'}
    sell, buy = [], []
    
    with st.spinner("Processing Market Data..."):
        for sym, key in tickers.items():
            try:
                df = yf.download(sym, period="300d", interval="1d", progress=False)
                if df.empty: continue
                px = df['Close'] if isinstance(df.columns,str) else df.xs('Close',axis=1,level=0).iloc[:,0]
                
                price, reason, action = get_signal(px, key)
                item = {'sym': key, 'price': price, 'reason': reason}
                
                if action=="SELL" and inv_data.get(key,True): sell.append(item)
                elif action=="BUY": buy.append(item)
            except: pass

    # --- RENDER SELL CARDS ---
    if sell:
        st.markdown("<div class='section' style='color:#e74c3c'>LIQUIDATION ORDER</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class="exec sell">
                <div>
                    <div class="asset-name">{x['sym']}</div>
                    <div class="asset-reason">{x['reason']}</div>
                </div>
                <div class="val-box">
                    <div class="val-main">${x['price']:,.2f}</div> <div class="val-sub tag-sell">MARKET PRICE</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- RENDER BUY CARDS (FIXED: PRICE INCLUDED) ---
    if buy:
        st.markdown("<div class='section' style='color:#2ecc71'>ACQUISITION TARGETS</div>", unsafe_allow_html=True)
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())
        
        for x in buy:
            sym = x['sym']
            if total_dana_usd > 1 and total_w > 0:
                usd = total_dana_usd * active[sym]/total_w
                if sym in ['BTC','GLD']: val, cur = f"Rp {usd*kurs_rupiah:,.0f}", "IDR"
                else: val, cur = f"${usd:,.2f}", "USD"
            else: val,cur="HOLD","-"

            # KARTU BUY DENGAN HARGA PASAR
            st.markdown(f"""
            <div class="exec buy">
                <div>
                    <div class="asset-name">{sym}</div>
                    <div class="market-price">${x['price']:,.2f}</div> <div class="asset-reason">{x['reason']}</div>
                </div>
                <div class="val-box">
                    <div class="val-main">{val}</div>
                    <div class="val-sub tag-buy">{cur}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy: st.info("System Stable. No Action Required.")
