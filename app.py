import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIG
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. WORLD-CLASS FINTECH UI (COMPLETE REDESIGN)
# =====================================================
st.markdown("""
<style>
/* CORE BLACK THEME - PERFECT PITCH BLACK */
.stApp { 
    background-color: #000000 !important; 
    color: #ffffff !important;
}
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stToolbar"] { visibility: hidden !important; }
.stTabs [data-baseweb="tab-list"] { background-color: #111111 !important; }

/* CONTAINER & LAYOUT */
.block-container {
    padding-top: 1rem !important;
    max-width: 1200px !important;
}
.st-emotion-cache-1r6z1ro { background-color: #000000 !important; }

/* TYPOGRAPHY - PRECISION FONTS */
h1, h2, h3, h4, h5, h6, .title { 
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", Inter, sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em;
}
.subtitle { 
    font-family: "SF Mono", Monaco, monospace !important;
    font-size: 12px !important;
    color: #888 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* PERFECT NUMBER INPUT - NO GAPS, FINTECH STYLE */
div[data-baseweb="input"] {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
    backdrop-filter: blur(20px) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[data-baseweb="input"]:hover {
    border-color: #4a90e2 !important;
    box-shadow: 0 8px 32px rgba(74, 144, 226, 0.15) !important;
}
div[data-baseweb="input"] input {
    color: #ffffff !important;
    background: transparent !important;
    border: none !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* STEPPER BUTTONS - SEAMLESS BLEND */
div[data-baseweb="button"] button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    width: 36px !important;
    height: 36px !important;
    margin: 0 4px !important;
}
div[data-baseweb="button"] button:hover {
    background: rgba(74, 144, 226, 0.2) !important;
    border-color: #4a90e2 !important;
}

/* EXECUTE BUTTON - HERO BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%) !important;
    border: none !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    padding: 20px 40px !important;
    height: 64px !important;
    box-shadow: 0 12px 40px rgba(74, 144, 226, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: none !important;
    letter-spacing: -0.01em;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 50px rgba(74, 144, 226, 0.4) !important;
    background: linear-gradient(135deg, #357abd 0%, #2a6099 100%) !important;
}

/* CAPTION - CLEAN */
[data-testid="caption"] {
    color: #666 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-bottom: 16px !important;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

/* RESULT CARDS - PROFESSIONAL FINTECH */
.sell-card {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
    border: 1px solid #ff4757 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin: 12px 0 !important;
    box-shadow: 0 8px 32px rgba(255, 71, 87, 0.15) !important;
}
.buy-card {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
    border: 1px solid #2ed573 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin: 12px 0 !important;
    box-shadow: 0 8px 32px rgba(46, 213, 115, 0.15) !important;
}
.stable-card {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f) !important;
    border: 1px solid #ffa502 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin: 12px 0 !important;
    box-shadow: 0 8px 32px rgba(255, 165, 2, 0.15) !important;
}

.card-symbol {
    font-size: 28px !important;
    font-weight: 800 !important;
    font-family: "SF Pro Display", Inter, sans-serif !important;
    margin-bottom: 8px !important;
}
.card-price {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #4ade80 !important;
    margin-bottom: 4px !important;
}
.card-reason {
    font-size: 14px !important;
    color: #aaa !important;
    font-family: "SF Mono", monospace !important;
}

/* TOGGLE SWITCHES - MODERN */
[data-baseweb="toggle"] {
    background: #333333 !important;
    border-radius: 20px !important;
}
[data-baseweb="toggle"] [data-baseweb="toggle-thumb"] {
    background: #666666 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}

/* SPINNER - CLEAN */
[data-testid="stSpinner"] {
    color: #4a90e2 !important;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .stButton > button { padding: 16px 24px !important; font-size: 16px !important; }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (LOCKED - DO NOT CHANGE)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try: return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except: return 16000.0
kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER - ENHANCED
# =====================================================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<div class='title' style='font-size: 36px; margin-bottom: 4px;'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>ARCHITECT: PETER • LIVE USD/IDR</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style='
        text-align: right; 
        font-size: 14px; 
        font-weight: 600; 
        color: #4ade80; 
        padding: 12px 0;
        background: rgba(74, 222, 128, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(74, 222, 128, 0.2);
    '>
        IDR {kurs_rupiah:,.0f}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# 5. INPUTS - WORLD CLASS LAYOUT
# =====================================================
st.markdown("<div class='caption'>CAPITAL CONFIGURATION</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
budget = col1.number_input("Target Capital ($)", value=300.0, step=10.0, format="%.0f")
used = col2.number_input("Capital Used ($)", value=0.0, step=10.0, format="%.0f")
extra = col3.number_input("Extra Capital ($)", value=0.0, step=10.0, format="%.0f")
total_dana_usd = (budget - used) + extra

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

st.markdown("<div class='caption'>INVENTORY CHECK (ON = EMPTY)</div>", unsafe_allow_html=True)
row1 = st.columns(3)
row2 = st.columns(2)
no_pltr = row1[0].toggle("🚀 PLTR", value=False)
no_qqq = row1[1].toggle("📈 QQQ", value=False)
no_btc = row1[2].toggle("₿ BTC", value=False)
no_gld = row2[0].toggle("🥇 GLD", value=False)
no_mstr = row2[1].toggle("🔥 MSTR", value=False)

inv_data = {'PLTR': not no_pltr, 'BTC': not no_btc, 'MSTR': not no_mstr, 'QQQ': not no_qqq, 'GLD': not no_gld}

# =====================================================
# 6. ENGINE (LOCKED - UNCHANGED)
# =====================================================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    cur_dd = (series - series.rolling(200, min_periods=1).max()).iloc[-1] / series.rolling(200, min_periods=1).max().iloc[-1]
    rsi = 100 - (100 / (1 + (series.diff().where(lambda x:x>0,0).rolling(14).mean() / (-series.diff().where(lambda x:x<0,0).rolling(14).mean()))))
    cur_rsi = rsi.iloc[-1]
    action, reason = "WAIT", "Stable"
    
    if cur_rsi > 80 or (price - sma200)/sma200 > 0.6: action, reason = "SELL", f"Overheat RSI {cur_rsi:.0f}"
    elif price > sma200: action, reason = "BUY", "Uptrend"
    elif (symbol=='PLTR' and cur_dd<-0.30) or (symbol in ['BTC','MSTR'] and cur_dd<-0.20): action, reason = "BUY", f"Dip {cur_dd*100:.0f}%"
    return price, reason, action

# =====================================================
# 7. EXECUTION - PROFESSIONAL CARDS
# =====================================================
st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

if st.button("🚀 RUN DIAGNOSTIC", use_container_width=True, type="primary"):
    tickers = {'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR', 'QQQ':'QQQ', 'GLD':'GLD'}
    sell, buy = [], []
    
    with st.spinner("🔍 Analyzing market signals..."):
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

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    if sell:
        st.markdown("## 🔴 LIQUIDATION REQUIRED")
        for x in sell:
            st.markdown(f"""
            <div class='sell-card'>
                <div class='card-symbol'>{x['sym']}</div>
                <div class='card-price'>${x['price']:,.2f}</div>
                <div class='card-reason'>SELL • {x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if buy:
        st.markdown("## 🟢 ACQUISITION TARGETS")
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())
        for x in buy:
            sym = x['sym']
            usd = total_dana_usd * active[sym]/total_w if total_w > 0 else 0
            val = f"Rp {usd*kurs_rupiah:,.0f}" if sym in ['BTC','GLD'] else f"${usd:,.2f}"
            st.markdown(f"""
            <div class='buy-card'>
                <div class='card-symbol'>{sym}</div>
                <div class='card-price'>{val}</div>
                <div class='card-reason'>BUY • {x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if not sell and not buy:
        st.markdown("""
        <div class='stable-card'>
            <div style='font-size: 32px; font-weight: 800; color: #ffa502; margin-bottom: 12px;'>⚖️</div>
            <div style='font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 8px;'>SYSTEM STABLE</div>
            <div style='font-size: 14px; color: #aaa; font-family: monospace;'>All positions balanced • No action required</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
