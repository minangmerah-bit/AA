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
# 2. UI STYLE (THE ZENITH - SURGICAL CLEAN)
# =====================================================
st.markdown("""
<style>
/* --- 1. CORE BLACK THEME --- */
.stApp {
    background-color: #000000 !important;
}
#MainMenu, header, footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}

/* --- 2. INPUT FIELDS (THE FIX) --- */
/* Kita tetap pakai Number Input agar keyboard HP otomatis angka */
/* Tapi kita hilangkan tombol +/- yang bikin bug visual */
div[data-testid="stNumberInputStepDown"] {display: none;}
div[data-testid="stNumberInputStepUp"] {display: none;}

/* Styling Kotak Input agar menyatu dengan background */
div[data-baseweb="input"] {
    background-color: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: white !important;
}
input {
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important; 
}

/* --- 3. TYPOGRAPHY --- */
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; color: white; }
.title { font-size: 26px; font-weight: 800; color: white; margin: 0; }
.subtitle { font-size: 11px; color: #666; letter-spacing: 1px; margin-bottom: 20px; }
.section-label { font-size: 10px; font-weight: 700; color: #555; letter-spacing: 1.2px; text-transform: uppercase; margin-top: 15px; margin-bottom: 5px; }

/* --- 4. EXECUTION CARDS (MINIMALIST) --- */
.card {
    background-color: #0a0a0a;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-buy { border-left: 3px solid #2ecc71; }
.card-sell { border-left: 3px solid #e74c3c; }

.card-sym { font-weight: 700; font-size: 16px; color: white; }
.card-sub { font-size: 11px; color: #666; }
.card-val { font-weight: 700; font-size: 16px; color: white; text-align: right; }
.card-tag { font-size: 10px; font-weight: 700; text-align: right; }
.tag-buy { color: #2ecc71; }
.tag-sell { color: #e74c3c; }

/* --- 5. BUTTON --- */
.stButton > button {
    width: 100%;
    background-color: white;
    color: black;
    font-weight: 800;
    border-radius: 8px;
    padding: 12px;
    border: none;
    margin-top: 10px;
}
.stButton > button:hover { background-color: #ddd; }
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
# 4. HEADER
# =====================================================
c1, c2 = st.columns([3,1])
with c1:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>ARCHITECT: PETER</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='text-align:right;font-size:10px;color:#555;padding-top:10px;font-family:monospace'>IDR {kurs_rupiah:,.0f}</div>", unsafe_allow_html=True)

# =====================================================
# 5. INPUTS (CLEAN & SIMPLE)
# =====================================================
st.markdown("<div class='section-label'>CAPITAL</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
# Step=0.0 mematikan spinner default, label_visibility collapsed membersihkan UI
budget = c1.number_input("Target", 300.0, step=0.0, label_visibility="collapsed")
used   = c2.number_input("Used", 0.0, step=0.0, label_visibility="collapsed")
extra  = c3.number_input("Extra", 0.0, step=0.0, label_visibility="collapsed")

# Label Manual di bawah (Lebih rapi)
c1.caption("Target ($)")
c2.caption("Used ($)")
c3.caption("Extra ($)")

total_dana_usd = (budget - used) + extra

st.markdown("<div class='section-label'>INVENTORY (ON = EMPTY)</div>", unsafe_allow_html=True)
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
    cur_dd = (series - series.rolling(200, min_periods=1).max()).iloc[-1] / series.rolling(200, min_periods=1).max().iloc[-1]
    rsi = 100 - (100 / (1 + (series.diff().where(lambda x:x>0,0).rolling(14).mean() / (-series.diff().where(lambda x:x<0,0).rolling(14).mean()))))
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
# 7. EXECUTION
# =====================================================
st.write("")
if st.button("RUN DIAGNOSTIC", use_container_width=True):
    tickers = {'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR', 'QQQ':'QQQ', 'GLD':'GLD'}
    sell, buy = [], []
    
    with st.spinner("Processing..."):
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

    st.write("")
    
    if sell:
        st.markdown("<div class='section-label' style='color:#e74c3c'>LIQUIDATION ORDER</div>", unsafe_allow_html=True)
        for x in sell:
            st.markdown(f"""
            <div class='card card-sell'>
                <div>
                    <div class='card-sym'>{x['sym']}</div>
                    <div class='card-sub'>${x['price']:,.2f} • {x['reason']}</div>
                </div>
                <div>
                    <div class='card-tag tag-sell'>SELL</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if buy:
        st.markdown("<div class='section-label' style='color:#2ecc71'>ACQUISITION TARGETS</div>", unsafe_allow_html=True)
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())
        
        for x in buy:
            sym = x['sym']
            if total_dana_usd > 1 and total_w > 0:
                pct = active[sym] / total_w
                amt_usd = total_dana_usd * pct
                if sym in ['BTC', 'GLD']:
                    val_txt = f"Rp {amt_usd*kurs_rupiah:,.0f}"
                    curr = "IDR"
                else:
                    val_txt = f"${amt_usd:,.2f}"
                    curr = "USD"
            else:
                val_txt, curr = "HOLD", "-"
            
            st.markdown(f"""
            <div class='card card-buy'>
                <div>
                    <div class='card-sym'>{sym}</div>
                    <div class='card-sub'>{x['reason']}</div>
                </div>
                <div>
                    <div class='card-val'>{val_txt}</div>
                    <div class='card-tag tag-buy'>{curr}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not sell and not buy:
        st.info("System Stable. No Action Required.")
