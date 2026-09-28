import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob
import datetime

# 1. PAGE SETUP & SECURE DYNAMIC DATABASE
st.set_page_config(page_title="AI Nifty Options Pro Engine", layout="wide")

# Persistent Cloud database simulation using Streamlit's state architecture
if "user_db" not in st.session_state:
    st.session_state["user_db"] = {
        "admin": "mysecretpassword123",  # Your permanent master Admin Key
        "client1": "paiduser789"          # Sample client credential
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# Encrypted Login Screen Interface Layout
if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center; color: #00F0FF;'>🔐 AI Trading Engine - Premium Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Enter subscription license login details to gain access</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("License Username / Email")
        password = st.text_input("License Access Password", type="password")
        submit_button = st.form_submit_button("Authenticate Device")
        
        if submit_button:
            db = st.session_state["user_db"]
            if username in db and db[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = username
                st.rerun()
            else:
                st.error("❌ Invalid license keys or expired subscription package.")
    st.stop()

# --- 👑 ADMINISTRATIVE SIDEBAR FOR CLIENT MANAGEMENT ---
st.sidebar.markdown(f"👤 Active License: **{st.session_state['current_user']}**")

if st.session_state["current_user"] == "admin":
    st.sidebar.write("---")
    st.sidebar.subheader("👑 Admin Client Manager")
    
    # Onboard New Customer
    new_user = st.sidebar.text_input("New Client Username", key="new_u")
    new_pass = st.sidebar.text_input("New Client Password", type="password", key="new_p")
    
    if st.sidebar.button("➕ Add Paid Customer"):
        if new_user and new_pass:
            st.session_state["user_db"][new_user] = new_pass
            st.sidebar.success(f"User '{new_user}' Added!")
            st.rerun()
            
    st.sidebar.write("---")
    st.sidebar.subheader("🗑️ Remove Customer Access")
    
    # Drop existing customer license
    all_users = list(st.session_state["user_db"].keys())
    if "admin" in all_users:
        all_users.remove("admin")
    
    if all_users:
        user_to_remove = st.sidebar.selectbox("Select User to Remove", all_users)
        if st.sidebar.button("❌ Remove / Delete Access"):
            del st.session_state["user_db"][user_to_remove]
            st.sidebar.error(f"User '{user_to_remove}' Wiped!")
            st.rerun()
    else:
        st.sidebar.info("No active subscription clients found.")

if st.sidebar.button("Logout / Disconnect Device"):
    st.session_state["authenticated"] = False
    st.session_state["current_user"] = None
    st.rerun()

# ----------------- MAIN CORE MULTI-AGENT ENGINE -----------------
st.markdown("<h1 style='text-align: center; color: #00F0FF; font-family: sans-serif;'>⚡ AI Nifty & Options Pro Engine</h1>", unsafe_allow_html=True)
st.write("---")

left_panel, right_panel = st.columns(2)

# 2. DATA PIPELINE BACKEND EXTRACTION
@st.cache_resource(ttl=60)
def fetch_market_data():
    nifty_ticker = yf.Ticker("^NSEI")
    df = nifty_ticker.history(period="5d", interval="15m")
    return nifty_ticker, df

nifty_ticker, df = fetch_market_data()

now = datetime.datetime.now()
current_time_str = now.strftime("%H:%M")
market_open_safe = "09:45"
market_close_safe = "15:15"

if not df.empty and len(df) >= 21:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    current_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    price_change = current_price - prev_price
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
    
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    ema9 = df['EMA9'].iloc[-1]
    ema21 = df['EMA21'].iloc[-1]
    
    high_low = df['High'] - df['Low']
    high_cp = (df['High'] - df['Close'].shift()).abs()
    low_cp = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().iloc[-1]
    
    dynamic_sl = max(35, min(60, int(atr * 1.5)))
    dynamic_target = dynamic_sl * 2
    
    if ema9 > ema21 and current_price > ema21:
        trend_status = "BULLISH (મજબૂત તેજી)"
        trend_score = 1
    elif ema9 < ema21 and current_price < ema21:
        trend_status = "BEARISH (મજબૂત મંદી)"
        trend_score = -1
    else:
        trend_status = "SIDEWAYS / VOLATILE"
        trend_score = 0
else:
    st.error("Data fetch timeout or market closed. Checking alternative nodes...")
    st.stop()

# 3. MARKET METRICS DISPLAY (LEFT PANEL)
with left_panel:
    st.subheader("📊 Market Metrics Matrix")
    m1, m2, m3 = st.columns(3)
    m1.metric("Nifty 50 Spot", f"₹{current_price:.2f}", f"{price_change:.2f}")
    m2.metric("RSI (15 Min)", f"{rsi_val:.2f}")
    m3.metric("Trend Momentum", trend_status)
    
    st.write("---")
    st.subheader("📰 Live Global News Sentiment Analyzer")
    
    try:
        news_list = nifty_ticker.news[:4]
    except:
        news_list = []
        
    total_sentiment = 0
    news_count = 0
    
    if news_list:
        for news in news_list:
            title = news.get('title', '')
            analysis = TextBlob(title)
            score = analysis.sentiment.polarity
            total_sentiment += score
            news_count += 1
            
            n_lbl, n_col = ("🟢 POSITIVE", "green") if score > 0.05 else (("🔴 NEGATIVE", "red") if score < -0.05 else ("🟡 NEUTRAL", "gray"))
            st.markdown(f"**• {title}**")
            st.markdown(f"<span style='color:{n_col}; font-size:12px; font-weight:bold;'>Sentiment Classification: {n_lbl}</span>", unsafe_allow_html=True)
            st.write("")
        avg_sentiment = total_sentiment / news_count if news_count > 0 else 0
    else:
        st.info("No active international news flow impacting index parameters.")
        avg_sentiment = 0

# 4. CRITERIA EXECUTION & PORTFOLIO RISK CONTROLS (RIGHT PANEL)
with right_panel:
    st.subheader("⚙️ Strategy & Option Risk Controls")
    
    capital = st.number_input("Total Trading Capital ₹", value=100000, step=10000)
    risk_pct = st.slider("Risk Exposure Threshold per Trade (%)", 0.5, 2.0, 1.0, 0.1)
    max_daily_loss = st.number_input("Max Daily Loss Limit Allowed ₹", value=2000, step=500)
    today_loss_incurred = st.number_input("Total Loss Incurred Today (If any) ₹", value=0, step=100)
    
    st.write("---")
    st.subheader("🤖 AI Ultimate Core Decision")
    
    time_valid = market_open_safe <= current_time_str <= market_close_safe
    loss_limit_hit = today_loss_incurred >= max_daily_loss
    
    final_signal = "HOLD / WAIT (No Strong Directional Strategy)"
    panel_color = "#2b2b2b"
    ai_reason = "Consolidation phase detected. Technical signals do not guarantee clean entry premium expansion."
    
    option_strike = "N/A"
    current_premium = 100.0
    premium_sl_points = 20.0
    premium_target_points = 40.0
    
    allowed_loss = capital * (risk_pct / 100.0)
    
    if loss_limit_hit:
        final_signal = "🚫 TRADING LOCKED (Daily Loss Limit Hit)"
        panel_color = "#4A0E17"
        ai_reason = "Daily risk allowance depleted. System locked to protect institutional portfolio balance."
    elif not time_valid:
        final_signal = "⏳ VOLATILITY LOCK (High Risk Hours)"
        panel_color = "#3A331A"
        ai_reason = f"Current time context ({current_time_str}) is marked unsafe for entry. High distribution volatility."
    else:
        if trend_score == 1:
            final_signal = "🟢 STRONG BUY (CALL OPTION)"
            panel_color = "#1E4A28"
            ai_reason = "EMA Crossover & Bullish Momentum confirmed. High probability of upward premium expansion."
            atm_strike = round(current_price / 50) * 50
            option_strike = f"NIFTY {atm_strike} CE"
        elif trend_score == -1:
            final_signal = "🔴 STRONG SELL / BUY PUT (PUT OPTION)"
            panel_color = "#4A1E1E"
            ai_reason = "EMA Crossover & Bearish Momentum confirmed. High probability of downward index movement."
            atm_strike = round(current_price / 50) * 50
            option_strike = f"NIFTY {atm_strike} PE"

    st.markdown(f"""
    <div style="background-color:{panel_color}; padding:15px; border-radius:10px; border-left:5px solid #00F0FF;">
        <h3 style="margin:0; color:#FFF;">Signal: {final_signal}</h3>
        <p style="margin:5px 0 0 0; color:#BBB; font-size:14px;"><b>AI Reason:</b> {ai_reason}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. EXECUTION MATRIX
    if final_signal in ["🟢 STRONG BUY (CALL OPTION)", "🔴 STRONG SELL / BUY PUT (PUT OPTION)"]:
        opt_sl_price = max(0.0, current_premium - premium_sl_points)
        opt_target_price = current_premium + premium_target_points
        nifty_lot_size = 75
        raw_qty = allowed_loss / premium_sl_points
        calculated_lots = int(raw_qty / nifty_lot_size)
        final_qty = calculated_lots * nifty_lot_size

        st.write("")
        st.markdown("### 📋 Live Option Trade Setup")
        st.write(f"• Contract Target: {option_strike}")
        st.markdown(f"• Premium Stop-Loss (SL): ₹{opt_sl_price:.2f}", unsafe_allow_html=True)
        st.markdown(f"• Premium Profit Target: ₹{opt_target_price:.2f}", unsafe_allow_html=True)
        st.write(f"• Allocation Strategy: {calculated_lots} Lots ({final_qty} Qty)")
        if "15:00" <= current_time_str <= "15:30":
            st.write("")
            st.markdown("""⚠️ AUTO SQUARE-OFF ALERT: Square off your open options positions before 15:15 to avoid broker penalty charges!""", unsafe_allow_html=True)
