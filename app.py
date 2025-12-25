import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURATION (IDENTITY: SYNTAX KERNEL) ---
st.set_page_config(
    page_title="SYNTAX KERNEL",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚫"
)

# --- CUSTOM CSS (DARK/MINIMALIST THEME) ---
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    h1 {
        font-family: 'Courier New', Courier, monospace;
        color: #ffffff;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    .stButton>button {
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #444;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #00ff00;
        color: #00ff00;
    }
    .metric-card {
        background-color: #1c1c1c;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("SYNTAX KERNEL // GRID SEARCH ENGINE")
st.markdown("`STATUS: ONLINE` | `MODE: EXHAUSTIVE COMPUTE` | `MODULE: STRATEGY OPTIMIZER`")
st.markdown("---")

# --- SIDEBAR: PARAMETER INPUT ---
st.sidebar.header("/// INPUT VECTOR")

ticker = st.sidebar.text_input("ASSET TICKER", value="BTC-USD").upper()
start_date = st.sidebar.date_input("START DATE", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("END DATE", value=pd.to_datetime("today"))
initial_capital = st.sidebar.number_input("INITIAL CAPITAL ($)", value=10000)

st.sidebar.markdown("---")
st.sidebar.header("/// GRID SEARCH SPACE")

# RSI Parameters Range
rsi_lower_start = st.sidebar.number_input("RSI Lower Start", value=20)
rsi_lower_end = st.sidebar.number_input("RSI Lower End", value=40)
rsi_step = st.sidebar.number_input("RSI Step", value=5)

# MA Parameters Range
ma_fast_start = st.sidebar.number_input("MA Fast Start", value=20)
ma_fast_end = st.sidebar.number_input("MA Fast End", value=50)
ma_step = st.sidebar.number_input("MA Step", value=10)

run_search = st.sidebar.button("INITIATE SYNTAX KERNEL")

# --- CORE LOGIC ---
def fetch_data(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"DATA FETCH ERROR: {e}")
        return None

def backtest_strategy(df, rsi_limit, ma_window, capital):
    # Copy data to avoid mutation
    data = df.copy()
    
    # Calculate Indicators
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['MA'] = ta.sma(data['Close'], length=ma_window)
    
    # Logic: Buy if RSI < Limit AND Price > MA (Trend Filter)
    data['Signal'] = 0
    data.loc[(data['RSI'] < rsi_limit) & (data['Close'] > data['MA']), 'Signal'] = 1 # BUY
    data.loc[data['RSI'] > 70, 'Signal'] = -1 # SELL (Simple Exit)
    
    # Position Simulation
    position = 0 # 0: Cash, 1: Invested
    balance = capital
    holdings = 0
    
    # Vectorized approach is harder for complex logic, using loop for clarity in backtest
    # For speed in grid search, we simplify:
    
    entry_dates = []
    exit_dates = []
    
    # Simulation Loop
    for i in range(1, len(data)):
        price = data['Close'].iloc[i]
        signal = data['Signal'].iloc[i]
        
        if position == 0 and signal == 1: # BUY
            holdings = balance / price
            balance = 0
            position = 1
            entry_dates.append(data.index[i])
            
        elif position == 1 and signal == -1: # SELL
            balance = holdings * price
            holdings = 0
            position = 0
            exit_dates.append(data.index[i])
            
    # Final Value
    final_val = balance if position == 0 else holdings * data['Close'].iloc[-1]
    ret = ((final_val - capital) / capital) * 100
    
    return final_val, ret

# --- EXECUTION ---
if run_search:
    data = fetch_data(ticker, start_date, end_date)
    
    if data is not None:
        st.write(f"**TARGET ACQUIRED:** {ticker} // **DATA POINTS:** {len(data)}")
        
        # Grid Generation
        rsi_range = range(rsi_lower_start, rsi_lower_end + 1, rsi_step)
        ma_range = range(ma_fast_start, ma_fast_end + 1, ma_step)
        
        results = []
        
        progress_bar = st.progress(0)
        total_iterations = len(rsi_range) * len(ma_range)
        iteration = 0
        
        status_text = st.empty()
        
        # GRID SEARCH LOOP
        for r in rsi_range:
            for m in ma_range:
                status_text.text(f"COMPUTING: RSI < {r} | MA {m}...")
                final_val, ret = backtest_strategy(data, r, m, initial_capital)
                results.append({
                    'RSI_Limit': r,
                    'MA_Window': m,
                    'Final_Balance': final_val,
                    'Return_%': ret
                })
                iteration += 1
                progress_bar.progress(iteration / total_iterations)
        
        status_text.text("COMPUTATION COMPLETE.")
        
        # Results Processing
        results_df = pd.DataFrame(results)
        best_result = results_df.loc[results_df['Return_%'].idxmax()]
        
        # --- OUTPUT DISPLAY ---
        st.markdown("### /// OPTIMIZATION RESULTS")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <small>BEST RETURN</small><br>
                <h2 style="color: #00ff00;">{best_result['Return_%']:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <small>OPTIMAL RSI LIMIT</small><br>
                <h2>{int(best_result['RSI_Limit'])}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <small>OPTIMAL MA WINDOW</small><br>
                <h2>{int(best_result['MA_Window'])}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### /// HEATMAP VISUALIZATION")
        
        # Pivot for Heatmap
        heatmap_data = results_df.pivot(index='RSI_Limit', columns='MA_Window', values='Return_%')
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis',
            text=np.round(heatmap_data.values, 2),
            texttemplate="%{text}%"
        ))
        
        fig.update_layout(
            title='PROFITABILITY MATRIX',
            xaxis_title='MA Window',
            yaxis_title='RSI Buy Limit',
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### /// RAW DATA LOG")
        st.dataframe(results_df.sort_values(by='Return_%', ascending=False), use_container_width=True)

    else:
        st.error("DATA FETCH FAILED. CHECK TICKER OR CONNECTION.")
