import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="9AM SYSTEM", 
    layout="centered"
)

# =====================================================
# 2. UI ARCHITECTURE (MOBILE RESPONSIVE FIXED)
# =====================================================
st.markdown("""
<style>
/* --- CORE CLEANUP --- */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}
.stApp { background-color: #000000 !important; }

/* --- ELIMINATE "PRESS ENTER" NOISE --- */
[data-testid="InputInstructions"] { display: none !important; }

/* --- CONTAINER --- */
.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 2rem; 
}

/* --- TYPOGRAPHY --- */
body { font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; color: white; }

/* --- INPUT ENGINEERING --- */
div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] { display: none !important; }

div[data-baseweb="input"] {
    background-color: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 8px 0;
}

input {
    color: white !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding-left: 15px !important;
    font-size: 18px !important;
}

.input-label {
    font-size: 11px; color: #888; font-weight: 600;
    margin-bottom: 6px; text-transform: uppercase;
    letter-spacing: 0.8px; text-align: left; padding-left: 2px;
}

/* --- HEADER FLEXBOX (SOLUSI MOBILE) --- */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-end; /* Rata bawah agar sejajar */
    width: 100%;
    margin-bottom: 15px; /* Jarak ke section bawah */
    border-bottom: 1px solid #1a1a1a; /* Garis tipis pemisah (opsional, biar rapi) */
    padding-bottom: 10px;
}

.header-left {
    display: flex;
    flex-direction: column;
}

.header-right {
    text-align: right;
    margin-bottom: 2px; /* Micro adjustment alignment */
}

.title { 
    font-size: 24px; 
    font-weight: 700; 
    color: white; 
    letter-spacing: -0.5px; 
    line-height: 1.2;
}

.subtitle {
    font-size: 10px; 
    color: #666; 
    font-family: "SF Mono", "Consolas", "Courier New", monospace; 
    font-style: italic; 
    letter-spacing: 1px; 
    margin-top: 2px;
    opacity: 0.8;
}

/* --- KURS INDICATOR STYLING --- */
.kurs-label { color: #555; font-weight: 600; font-size: 11px; letter-spacing: 0.5px; }
.kurs-value { color: #4caf50; font-weight: 700; font-size: 13px; font-family: monospace; }

/* --- SECTION TITLE --- */
.section {
    margin-top: 0.5rem; /* RAPATKAN GAP */
    font-size: 10px; 
    letter-spacing: 1.5px;
    color: #555; 
    text-transform: uppercase; 
    font-weight: 700; 
    margin-bottom: 10px;
}

/* --- INTELLIGENT CARDS --- */
.exec {
    background-color: #0a0a0a;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.buy { border-left: 4px solid #2ecc71; }    
.sell { border-left: 4px solid #e74c3c; }   
.hold { border-left: 4px solid #555555; }   

.asset-name { font-weight: 800; font-size: 17px; color: white; margin-bottom: 2px; }
.market-price { font-size: 13px; color: #eee; font-weight: 600; font-family: monospace; }
.asset-reason { font-size: 10px; color: #666; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px;}

.val-box { text-align: right; }

.action-tag {
    font-size: 10px; font-weight: 800; letter-spacing: 1.2px;
    text-transform: uppercase; margin-bottom: 2px; display: block;
}
.tag-text-buy { color: #2ecc71; }
.tag-text-sell { color: #e74c3c; }
.tag-text-hold { color: #777; } 

.val-main { font-weight: 800; font-size: 16px; color: white; }
.val-sub { font-size: 10px; font-weight: 700; color: #555; letter-spacing: 0.5px; margin-top: 2px;}

/* --- BUTTON --- */
.stButton > button {
    width: 100%; background: white; color: black; font-weight: 800;
    border-radius: 8px; padding: 14px 0; font-size: 14px;
    border: none; margin-top: 30px;
}
.stButton > button:hover { background: #cccccc; transform: scale(0.99); }

/* --- MOBILE OPTIMIZATION --- */
@media only screen and (max-width: 600px) {
    .header-container {
        align-items: flex-start; /* Pada HP, biar rapi */
    }
    .header-right {
        margin-top: 5px; /* Sedikit jarak jika layar sangat sempit */
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (PETER PROTOCOL - LOCKED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try: return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except: return 16000.0
kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER UI (SINGLE BLOCK HTML - NO COLUMNS)
# =====================================================
# Menggunakan satu container HTML agar menyatu di Mobile
st.markdown(f"""
<div class="header-container">
    <div class="header-left">
        <div class="title">9AM SYSTEM</div>
        <div class="subtitle">ARCHITECT BY rizqynandaputra</div>
    </div>
    <div class="header-right">
        <span class="kurs-label">KURS : </span>
        <span class="kurs-value">{kurs_rupiah:,.0f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    rolling_max = series.rolling(200, min_periods=1).max()
    cur_dd = (series - rolling_max).iloc[-1] / rolling_max.iloc[-1]
    
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    cur_rsi = rsi.iloc[-1]

    action, reason = "WAIT", "Stable"

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
                    <div class="action-tag tag-text-sell">SELL NOW</div>
                    <div class="val-main">${x['price']:,.2f}</div>
                    <div class="val-sub">MARKET PRICE</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if buy:
        has_funds = total_dana_usd > 1
        header_color = "#2ecc71" if has_funds else "#777"
        header_text = "ACQUISITION TARGETS" if has_funds else "WATCHLIST (NO FUNDS)"
        
        st.markdown(f"<div class='section' style='color:{header_color}'>{header_text}</div>", unsafe_allow_html=True)
        
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())
        
        for x in buy:
            sym = x['sym']
            if has_funds and total_w > 0:
                usd = total_dana_usd * active[sym]/total_w
                if sym in ['BTC','GLD']: val, cur = f"Rp {usd*kurs_rupiah:,.0f}", "IDR"
                else: val, cur = f"${usd:,.2f}", "USD"
                card_class, tag_class, tag_label = "buy", "tag-text-buy", "BUY"
            else:
                val, cur = "0.00", "-"
                card_class, tag_class, tag_label = "hold", "tag-text-hold", "HOLD"
            
            st.markdown(f"""
            <div class="exec {card_class}">
                <div>
                    <div class="asset-name">{sym}</div>
                    <div class="market-price">${x['price']:,.2f}</div>
                    <div class="asset-reason">{x['reason']}</div>
                </div>
                <div class="val-box">
                    <div class="action-tag {tag_class}">{tag_label}</div>
                    <div class="val-main">{val}</div>
                    <div class="val-sub">{cur}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy: st.info("System Stable. No Action Required.")
