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
# 2. INSTITUTIONAL CSS - SILENT LUXURY
# =====================================================
st.markdown("""
<style>
/* CORE INSTITUTIONAL BLACK */
.stApp { background-color: #000000 !important; color: #ffffff !important; }
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stToolbar"] { visibility: hidden !important; }

/* CONTAINER */
.block-container { padding: 2rem 1rem !important; max-width: 1200px !important; }

/* TYPOGRAPHY - BLOOMBERG TERMINAL */
* { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", Inter, sans-serif !important; }
.title { font-size: 32px !important; font-weight: 600 !important; color: #ffffff !important; letter-spacing: -0.02em; }
.subtitle { font-size: 13px !important; color: #888 !important; font-weight: 500 !important; letter-spacing: 0.5px; text-transform: uppercase; }

/* INPUT FIELDS - SEAMLESS MATTE */
div[data-baseweb="input"] {
    background: #111111 !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    transition: border-color 0.2s ease !important;
}
div[data-baseweb="input"]:hover { border-color: #666666 !important; }
div[data-baseweb="input"] input {
    color: #ffffff !important;
    background: transparent !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    padding: 0 !important;
}

/* EXECUTE BUTTON - INSTITUTIONAL */
.stButton > button {
    background: #222222 !important;
    border: 1px solid #444444 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 18px 32px !important;
    height: 60px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.5px;
}
.stButton > button:hover {
    background: #333333 !important;
    border-color: #666666 !important;
    transform: none !important;
}

/* CAPTION */
[data-testid="caption"] {
    color: #888 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    margin-bottom: 16px !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* TOGGLE - MINIMAL */
[data-baseweb="toggle"] { background: #333333 !important; border-radius: 20px !important; }
[data-baseweb="toggle"] [data-baseweb="toggle-thumb"] { 
    background: #666666 !important; 
    box-shadow: none !important; 
    width: 24px !important; 
    height: 24px !important; 
}

/* RESULT CARDS - LEFT BORDER ONLY */
.signal-card {
    background: #111111 !important;
    border-left: 4px solid transparent !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 24px !important;
    margin: 12px 0 !important;
    border-top: 1px solid #333333 !important;
    border-right: 1px solid #333333 !important;
    border-bottom: 1px solid #333333 !important;
}
.sell-card { border-left-color: #ff6b6b !important; }
.buy-card { border-left-color: #51cf66 !important; }
.stable-card { border-left-color: #ffd43b !important; }

.card-header { 
    font-size: 20px !important; 
    font-weight: 600 !important; 
    color: #ffffff !important; 
    margin-bottom: 12px !important; 
}
.card-price { 
    font-size: 28px !important; 
    font-weight: 700 !important; 
    color: #ffffff !important; 
    margin-bottom: 4px !important; 
}
.card-reason { 
    font-size: 14px !important; 
    color: #aaa !important; 
    font-weight: 500 !important; 
}

/* STATUS BAR */
.status-bar {
    background: #111111 !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    text-align: center !important;
}

/* SPACING */
.stDivider { height: 1px !important; background-color: #333333 !important; margin: 24px 0 !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (LOCKED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try: return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except: return 16000.0
kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER
# =====================================================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="title">EXECUTOR X1</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">ARCHITECT: PETER</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style='
        background: #111111; 
        border: 1px solid #333333; 
        border-radius: 8px; 
        padding: 16px; 
        text-align: center; 
        font-size: 16px; 
        font-weight: 600; 
        color: #ffffff;
    '>
        IDR {kurs_rupiah:,.0f}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# 5. INPUTS - TEXT_INPUT (SEAMLESS)
# =====================================================
st.caption("CAPITAL CONFIGURATION")
col1, col2, col3 = st.columns(3)
budget_input = col1.text_input("Target ($)", value="300", key="budget")
used_input = col2.text_input("Used ($)", value="0", key="used") 
extra_input = col3.text_input("Extra ($)", value="0", key="extra")

try:
    budget = float(budget_input) if budget_input else 300.0
    used = float(used_input) if used_input else 0.0
    extra = float(extra_input) if extra_input else 0.0
except:
    budget, used, extra = 300.0, 0.0, 0.0

total_dana_usd = (budget - used) + extra

st.caption("INVENTORY CHECK (ON = EMPTY)")
row1 = st.columns(3)
row2 = st.columns(2)
no_pltr = row1[0].toggle("PLTR", value=False)
no_qqq = row1[1].toggle("QQQ", value=False)
no_btc = row1[2].toggle("BTC", value=False)
no_gld = row2[0].toggle("GLD", value=False)
no_mstr = row2[1].toggle("MSTR", value=False)

inv_data = {'PLTR': not no_pltr, 'BTC': not no_btc, 'MSTR': not no_mstr, 'QQQ': not no_qqq, 'GLD': not no_gld}

st.divider()

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
# 7. EXECUTION - INSTITUTIONAL CARDS
# =====================================================
if st.button("RUN DIAGNOSTIC", use_container_width=True):
    tickers = {'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR', 'QQQ':'QQQ', 'GLD':'GLD'}
    sell, buy = [], []
    
    with st.spinner("Analyzing signals..."):
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

    if sell:
        st.markdown("### LIQUIDATION REQUIRED")
        for x in sell:
            st.markdown(f"""
            <div class='signal-card sell-card'>
                <div class='card-header'>SELL {x['sym']}</div>
                <div class='card-price'>${x['price']:,.2f}</div>
                <div class='card-reason'>{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if buy:
        st.markdown("### ACQUISITION TARGETS")
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())
        for x in buy:
            sym = x['sym']
            usd = total_dana_usd * active[sym]/total_w if total_w > 0 else 0
            val = f"Rp {usd*kurs_rupiah:,.0f}" if sym in ['BTC','GLD'] else f"${usd:,.2f}"
            st.markdown(f"""
            <div class='signal-card buy-card'>
                <div class='card-header'>BUY {sym}</div>
                <div class='card-price'>{val}</div>
                <div class='card-reason'>{x['reason']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if not sell and not buy:
        st.markdown("""
        <div class='signal-card stable-card'>
            <div class='card-header'>SYSTEM STABLE</div>
            <div class='card-reason'>All positions balanced. No action required.</div>
        </div>
        """, unsafe_allow_html=True)
