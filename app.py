import streamlit as st
import yfinance as yf

# =====================================================
# 1. SYSTEM CONFIG
# =====================================================
st.set_page_config(
    page_title="Executor X1",
    layout="centered"
    # Page Icon menggunakan default Streamlit (Netral/Kosong)
)

# =====================================================
# 2. UI STYLE (MATTE BLACK, LEFT LABELS, CENTER INPUT)
# =====================================================
st.markdown("""
<style>
/* HIDE STREAMLIT DEFAULT ELEMENTS */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}

/* CORE THEME: PITCH BLACK */
.stApp {
    background-color: #000000 !important;
}

/* CONTAINER LAYOUT */
.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* GLOBAL FONT */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    color: white;
}

/* --- INPUT FIELD ENGINEERING --- */
/* 1. HILANGKAN TOMBOL +/- (Stepper) */
div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] {
    display: none !important;
}

/* 2. STYLING KOTAK INPUT */
div[data-baseweb="input"] {
    background-color: #111 !important; /* Abu Gelap Matte */
    border: 1px solid #333 !important; /* Border Halus */
    border-radius: 8px !important;
    color: white !important;
    padding: 8px 0; /* Padding vertikal agar kotak terlihat kokoh */
}

/* 3. TEKS DI DALAM INPUT (ANGKA) */
input {
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important; /* Angka tetap di tengah (Hero Value) */
    font-size: 18px !important;
}

/* 4. LABEL KUSTOM (JUDUL DI ATAS KOTAK) */
.input-label {
    font-size: 11px;
    color: #888; /* Abu terang agar kontras tapi tidak menyilaukan */
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    text-align: left; /* RATA KIRI SESUAI REQUEST */
    padding-left: 2px;
}

/* HEADER STYLE */
.title {
    font-size: 24px;
    font-weight: 700;
    color: white;
    letter-spacing: -0.5px;
}
.subtitle {
    font-size: 12px;
    color: #666;
    font-family: "SF Mono", "Roboto Mono", monospace; /* Coding Signature Style */
    margin-top: 4px;
}

/* SECTION HEADERS */
.section {
    margin-top: 2.5rem;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #555;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 15px;
}

/* EXECUTION CARDS */
.exec {
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
    border: 1px solid #222;
    background-color: #050505;
}

.buy { border-left: 3px solid #2ecc71; }
.sell { border-left: 3px solid #e74c3c; }

.exec-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* CARD TYPOGRAPHY */
.asset { font-weight: 700; font-size: 15px; color: white; }
.price { font-size: 11px; color: #888; margin-top: 2px; }
.action-sell { font-weight: 800; color: #e74c3c; font-size: 13px; }
.value { font-weight: 700; font-size: 15px; color: white; }
.currency { font-size: 10px; color: #888; text-align: right; }
.reason { font-size: 10px; color: #666; margin-top: 6px; padding-top:6px; border-top: 1px solid #1a1a1a; text-transform: uppercase; }

/* BUTTON STYLE */
.stButton > button {
    width: 100%;
    background: white;
    color: black;
    font-weight: 800;
    border-radius: 8px;
    padding: 14px 0;
    font-size: 14px;
    border: none;
    margin-top: 25px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #cccccc;
    transform: scale(0.99);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FX LOGIC (PETER PROTOCOL - LOCKED & VALIDATED)
# =====================================================
@st.cache_data(ttl=3600)
def get_usd_idr():
    try:
        return yf.Ticker("IDR=X").history(period="1d")['Close'].iloc[-1]
    except:
        return 16000.0

kurs_rupiah = get_usd_idr()

# =====================================================
# 4. HEADER (IDENTITY: rizqynandaputra)
# =====================================================
l, r = st.columns([3,1])
with l:
    st.markdown("<div class='title'>EXECUTOR X1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>rizqynandaputra</div>", unsafe_allow_html=True)
with r:
    st.markdown(
        f"<div style='text-align:right;font-size:11px;color:#555;padding-top:10px;font-family:monospace'>IDR {kurs_rupiah:,.0f}</div>",
        unsafe_allow_html=True
    )

# =====================================================
# 5. INPUT SECTION (PERFECT ALIGNMENT)
# =====================================================
st.markdown("<div class='section'>CAPITAL CONFIGURATION</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    # Label Manual (HTML) Rata Kiri
    st.markdown("<div class='input-label'>TARGET ($)</div>", unsafe_allow_html=True)
    # Input Streamlit (Angka Tengah, Tanpa Label Bawaan)
    budget = st.number_input("Target", 300.0, step=0.0, label_visibility="collapsed")

with c2:
    st.markdown("<div class='input-label'>USED ($)</div>", unsafe_allow_html=True)
    used = st.number_input("Used", 0.0, step=0.0, label_visibility="collapsed")

with c3:
    st.markdown("<div class='input-label'>EXTRA ($)</div>", unsafe_allow_html=True)
    extra = st.number_input("Extra", 0.0, step=0.0, label_visibility="collapsed")

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
# 6. ENGINE CORE (DO NOT MODIFY)
# =====================================================
def get_signal(series, symbol):
    price = series.iloc[-1]
    sma200 = series.rolling(200).mean().iloc[-1]
    
    # 1. DRAWDOWN CALCULATION (For Dip Buying)
    # Menghitung persentase jatuh dari titik tertinggi 200 hari terakhir
    rolling_max = series.rolling(200, min_periods=1).max()
    cur_dd = (series - rolling_max).iloc[-1] / rolling_max.iloc[-1]
    
    # 2. RSI CALCULATION (For Overheat/Sell)
    # RSI 14 Periode Standar
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    cur_rsi = rsi.iloc[-1]

    action, reason = "WAIT", "Stable"

    # 3. DECISION MATRIX (HIERARCHY)
    # A. SELL SIGNAL (Priority 1): RSI Overheat (>80) atau Harga terlalu jauh dari SMA (>60%)
    if cur_rsi > 80 or (price - sma200)/sma200 > 0.6:
        action, reason = "SELL", f"Overheat RSI {cur_rsi:.0f}"
    
    # B. BUY TREND (Priority 2): Harga di atas SMA200 (Uptrend aman)
    elif price > sma200:
        action, reason = "BUY", "Uptrend"
    
    # C. BUY DIP (Priority 3): Crash Detection
    # PLTR diskon 30%, BTC/MSTR diskon 20%
    elif (symbol=='PLTR' and cur_dd < -0.30) or (symbol in ['BTC','MSTR'] and cur_dd < -0.20):
        action, reason = "BUY", f"Dip {cur_dd*100:.0f}%"

    return price, reason, action

# =====================================================
# 7. EXECUTION LOOP
# =====================================================
st.write("")
if st.button("RUN DIAGNOSTIC", use_container_width=True):

    tickers = {
        'PLTR':'PLTR', 'BTC-USD':'BTC', 'MSTR':'MSTR',
        'QQQ':'QQQ', 'GLD':'GLD'
    }

    sell, buy = [], []

    with st.spinner("Processing Market Data..."):
        for sym, key in tickers.items():
            try:
                # Download Data 300 Hari (Cukup untuk SMA200 + Buffer)
                df = yf.download(sym, period="300d", interval="1d", progress=False)
                if df.empty: continue

                # Extract Series Close
                px = df['Close'] if isinstance(df.columns,str) else df.xs('Close',axis=1,level=0).iloc[:,0]
                
                # Get Signal
                price, reason, action = get_signal(px, key)

                item = {'sym': key, 'price': price, 'reason': reason}
                
                # Filter Logic:
                # Sell hanya jika barang ada di inventory
                if action=="SELL" and inv_data.get(key,True):
                    sell.append(item)
                # Buy ditampung dulu untuk pembobotan
                elif action=="BUY":
                    buy.append(item)
            except: pass

    # --- RENDER OUTPUT: SELL ---
    if sell:
        st.markdown("<div class='section' style='color:#e74c3c'>LIQUIDATION ORDER</div>", unsafe_allow_html=True)
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

    # --- RENDER OUTPUT: BUY ---
    if buy:
        st.markdown("<div class='section' style='color:#2ecc71'>ACQUISITION TARGETS</div>", unsafe_allow_html=True)

        # Weighting System (Bobot Portofolio)
        base_w = {'BTC':0.2,'MSTR':0.2,'PLTR':0.35,'QQQ':0.15,'GLD':0.1}
        
        # Hitung Total Bobot Aktif (Hanya aset yang sinyalnya BUY)
        active = {x['sym']:base_w.get(x['sym'],0) for x in buy}
        total_w = sum(active.values())

        for x in buy:
            sym = x['sym']
            # Alokasi Dana Proporsional
            if total_dana_usd > 1 and total_w > 0:
                usd = total_dana_usd * active[sym]/total_w
                # Konversi Mata Uang Visual
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
