import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob
import datetime
import time
from gtts import gTTS
import base64

# 1. PREMIUM PAGE SETUP WITH CUSTOM CSS CANVAS
st.set_page_config(page_title="DIAGNA | AI Options Engine", page_icon="⚡", layout="wide")

# Custom Professional CSS Injector for High-End Dashboard Styling
st.markdown("""
<style>
    body { background-color: #0E1117; color: #E2E8F0; }
    .stApp { background: linear-gradient(135deg, #0e1118 0%, #07090e 100%); }
    .stNumberInput div, .stSlider div { background-color: #1A1F2C !important; border-radius: 8px !important; }
    .metric-card { background: #131722; padding: 20px; border-radius: 12px; border: 1px solid #2A2E39; box-shadow: 0 4px 15px rgba(0,0,0,0.3); text-align: center; }
    .metric-val { font-size: 24px; font-weight: bold; color: #00F0FF; margin-top: 5px; }
    .metric-lbl { font-size: 13px; color: #848E9C; font-weight: 500; text-transform: uppercase; }
    .news-card { background: #1A1F2C; padding: 12px; border-radius: 8px; border-left: 4px solid #00F0FF; margin-bottom: 10px; }
    .welcome-banner { background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%); padding: 2px; border-radius: 10px; text-align: center; color: white; margin-bottom: 25px; }
    .welcome-inner { background: #0E1117; padding: 15px; border-radius: 9px; }
</style>
""", unsafe_allow_html=True)

# --- ✨ STARTING SPLASH SCREEN ANIMATION (DIAGNA CREATED) ---
if "splash_done" not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; font-family: sans-serif;'>
            <h1 style='color: #00F0FF; font-size: 50px; font-weight: 800; letter-spacing: 5px; text-shadow: 0 0 20px #00F0FF;'>DIAGNA</h1>
            <p style='color: #848E9C; font-size: 16px; letter-spacing: 3px;'>💎 CREATED BY DISHANT 💎</p>
            <br>
            <div style='color: #4364F7; font-size: 14px;'>🧬 Loading Quantum Multi-Agent Systems...</div>
        </div>
        """, unsafe_allow_html=True)
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.015)
            progress_bar.progress(percent_complete + 1)
    splash.empty()
    st.session_state["splash_done"] = True

# Persistent Cloud database architecture
if "user_db" not in st.session_state:
    st.session_state["user_db"] = {
        "dishant": "dishant911",
        "client1": "paiduser789"
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# --- 🔐 AUTOMATED SINGLE-CLICK LOGON MATRIX ---
if not st.session_state["authenticated"] and "auth_user" in st.query_params:
    q_user = st.query_params["auth_user"]
    if q_user in st.session_state["user_db"]:
        st.session_state["authenticated"] = True
        st.session_state["current_user"] = q_user

# Professional Dynamic Login Layout
if not st.session_state["authenticated"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h2 style='color: #00F0FF; margin: 0;'>🔐 DIAGNA PROTOCOL</h2>
            <p style='color: #64748B; font-size: 13px;'>Secure License Verification Terminal</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("License ID")
            password = st.text_input("Secret Token", type="password")
            submit_button = st.form_submit_button("Access Secure Shell")
            
            if submit_button:
                db = st.session_state["user_db"]
                if username in db and db[username] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = username
                    st.query_params["auth_user"] = username
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Revoked or Invalid License Security Patch.")
    st.stop()
    # --- 👑 ADMINISTRATIVE SIDEBAR CONTROL CENTER ---
st.sidebar.markdown(f"🧬 Active Terminal Node: **{st.session_state['current_user'].upper()}**")

if st.session_state["current_user"] in ["admin", "dishant"]:
    st.sidebar.write("---")
    st.sidebar.subheader("👑 System Access Control")
    new_user = st.sidebar.text_input("Client ID", key="new_u")
    new_pass = st.sidebar.text_input("Client Secret", type="password", key="new_p")
    
    if st.sidebar.button("➕ Inject Client License"):
        if new_user and new_pass:
            st.session_state["user_db"][new_user] = new_pass
            st.sidebar.success(f"License Key Registered for {new_user}")
            st.rerun()
            
    st.sidebar.write("---")
    all_users = list(st.session_state["user_db"].keys())
    for master in ["admin", "dishant"]:
        if master in all_users: all_users.remove(master)
    
    if all_users:
        user_to_remove = st.sidebar.selectbox("Revoke License Scope", all_users)
        if st.sidebar.button("❌ Terminate License"):
            del st.session_state["user_db"][user_to_remove]
            st.sidebar.error(f"Access Pipeline Wiped for {user_to_remove}")
            st.rerun()

if st.sidebar.button("Disconnect Terminal Session"):
    st.session_state["authenticated"] = False
    st.session_state["current_user"] = None
    st.session_state.pop("splash_done", None) 
    if "auth_user" in st.query_params:
        del st.query_params["auth_user"]  # Wipe parameters on safe manual logout
    st.rerun()

# ----------------- MAIN PROFESSIONAL CANVAS -----------------
st.markdown("""
<div class='welcome-banner'>
    <div class='welcome-inner'>
        <h1 style='margin:0; color:#00F0FF; font-size:28px; font-family:sans-serif; letter-spacing: 2px;'>⚡ DIAGNA QUANTUM OPTIONS ENGINE ⚡</h1>
        <p style='margin:5px 0 0 0; color:#848E9C; font-size:12px;'>Institutional Grade Analytics Framework for Nifty 50 Contracts</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. DATA PIPELINE BACKGROUND INTEGRITY EXTRACTION
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
        trend_status, trend_score, trend_color = "BULLISH (મજબૂત તેજી)", 1, "#02C076"
    elif ema9 < ema21 and current_price < ema21:
        trend_status, trend_score, trend_color = "BEARISH (મજબૂત મંદી)", -1, "#E44B4B"
    else:
        trend_status, trend_score, trend_color = "SIDEWAYS ZONE", 0, "#848E9C"
else:
    st.error("🔒 Pipeline Interrupted: Market Feed node timeout. Re-establishing link...")
    st.stop()

# MAIN ROW SPLIT
left_panel, right_panel = st.columns([1.1, 1])

# 3. METRICS MATRIX INTERFACE (LEFT)
with left_panel:
    st.markdown("<h3 style='color: #E2E8F0; font-size:18px;'>📊 Live Market Telemetry</h3>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    
    chg_prefix = "+" if price_change >= 0 else ""
    chg_color = "#02C076" if price_change >= 0 else "#E44B4B"
    
    with m_col1:
        st.markdown(f"""<div class='metric-card'><div class='metric-lbl'>Nifty 50 Spot</div><div class='metric-val'>₹{current_price:.2f}</div><div style='color:{chg_color}; font-size:12px; margin-top:2px;'>{chg_prefix}{price_change:.2f}</div></div>""", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""<div class='metric-card'><div class='metric-lbl'>RSI (15M Oscillator)</div><div class='metric-val'>{rsi_val:.2f}</div><div style='color:#848E9C; font-size:12px; margin-top:2px;'>Momentum Filter</div></div>""", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""<div class='metric-card'><div class='metric-lbl'>Core Architecture</div><div class='metric-val' style='color:{trend_color}; font-size:15px; padding-top:6px;'>{trend_status}</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br><h3 style='color: #E2E8F0; font-size:18px;'>📰 Global Sentiment Node Analyzer</h3>", unsafe_allow_html=True)
    try:
        news_list = nifty_ticker.news[:3]
    except:
        news_list = []
        
    if news_list:
        for news in news_list:
            title = news.get('title', '')
            analysis = TextBlob(title)
            score = analysis.sentiment.polarity
            n_lbl, n_col = ("🟢 BULLISH FLOW", "#02C076") if score > 0.05 else (("🔴 BEARISH FLOW", "#E44B4B") if score < -0.05 else ("🟡 NEUTRAL MARKET", "#848E9C"))
            
            st.markdown(f"""
            <div class='news-card'>
                <div style='font-size:13px; font-weight:600; color:#E2E8F0;'>• {title}</div>
                <div style='color:{n_col}; font-size:11px; font-weight:bold; margin-top:4px;'>AI Tag: {n_lbl}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No volatile structural news flow affecting baseline tracking nodes.")
        # --- 📊 LIVE TRADINGVIEW CHART CANVAS ---
    st.markdown("<br><h3 style='color: #E2E8F0; font-size:18px;'>📈 Nifty 50 Real-Time Chart Canvas</h3>", unsafe_allow_html=True)
    
    # TradingView HTML Widget Embedded securely
    tradingview_html = """
    <div class="tradingview-widget-container" style="height:350px;">
      <div id="tradingview_nifty"></div>
      <script type="text/javascript" src="https://tradingview.com"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "NSE:NIFTY",
        "interval": "15",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_nifty"
      });
      </script>
    </div>
    """
    st.components.v1.html(tradingview_html, height=360)

# 4. CRITERIA EXECUTION PANEL (RIGHT)
with right_panel:
    st.markdown("<h3 style='color: #E2E8F0; font-size:18px;'>⚙️ Capital Matrix & Risk Parameter Config</h3>", unsafe_allow_html=True)
    
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        capital = st.number_input("Institutional Capital (₹)", value=100000, step=10000)
        max_daily_loss = st.number_input("Max Daily Allocation Threshold (₹)", value=2000, step=500)
    with r_col2:
        risk_pct = st.slider("Risk Multiplier Per Trade (%)", 0.5, 2.0, 1.0, 0.1)
        today_loss_incurred = st.number_input("Incurred Drawdown Logs (₹)", value=0, step=100)
        
    st.markdown("<br><h3 style='color: #E2E8F0; font-size:18px;'>🤖 DIAGNA AI Neural Core Decision</h3>", unsafe_allow_html=True)
    
    time_valid = market_open_safe <= current_time_str <= market_close_safe
    loss_limit_hit = today_loss_incurred >= max_daily_loss
    
    final_signal = "STABLE HOLD / WAIT"
    panel_color = "#1E222D"
    panel_border = "#2A2E39"
    ai_reason = "Consolidation phase matrix. Signal parameters do not justify directional risk exposure."
    
    option_strike = "N/A"
    current_premium = 100.0
    premium_sl_points = 20.0
    premium_target_points = 40.0
    allowed_loss = capital * (risk_pct / 100.0)
    
    if loss_limit_hit:
        final_signal = "🚫 RISK EXPOSURE LOCKDOWN"
        panel_color = "#2D191E"
        panel_border = "#E44B4B"
        ai_reason = "Daily risk allowance completely depleted. System firewall engaged to protect account equity."
    elif not time_valid:
        final_signal = "⏳ VOLATILITY SAFELOCK ACTIVATED"
        panel_color = "#2A2415"
        panel_border = "#F3BA2F"
        ai_reason = f"Current system time context ({current_time_str}) is restricted. Safe window is 09:45 - 15:15."
    else:
        if trend_score == 1:
            final_signal = "🟢 ORDER EXECUTION: BUY CALL CONTRACT (CE)"
            panel_color = "#102A1E"
            panel_border = "#02C076"
            ai_reason = "EMA Golden Cross & Bullish Aggression confirmed. Favorable probability for premium momentum."
            atm_strike = round(current_price / 50) * 50
            option_strike = f"NIFTY {atm_strike} CE"
        elif trend_score == -1:
            final_signal = "🔴 ORDER EXECUTION: BUY PUT CONTRACT (PE)"
            panel_color = "#321919"
            panel_border = "#E44B4B"
            ai_reason = "EMA Bearish Divergence & Short Expansion confirmed. Downward velocity acceleration matrix."
            atm_strike = round(current_price / 50) * 50
            option_strike = f"NIFTY {atm_strike} PE"

    st.markdown(f"""
    <div style="background-color:{panel_color}; padding:18px; border-radius:12px; border:1px solid {panel_border}; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h4 style="margin:0; color:#FFF; font-size:16px;">{final_signal}</h4>
        <p style="margin:6px 0 0 0; color:#B2B8C4; font-size:12px; line-height:1.4;"><b>System Logic Node:</b> {ai_reason}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. RISK EXECUTION CALCULATION OVERLAY
    if final_signal in ["🟢 ORDER EXECUTION: BUY CALL CONTRACT (CE)", "🔴 ORDER EXECUTION: BUY PUT CONTRACT (PE)"]:
        opt_sl_price = max(0.0, current_premium - premium_sl_points)
        opt_target_price = current_premium + premium_target_points
        nifty_lot_size = 75
        raw_qty = allowed_loss / premium_sl_points
        calculated_lots = int(raw_qty / nifty_lot_size)
        final_qty = calculated_lots * nifty_lot_size

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#131722; padding:15px; border-radius:10px; border:1px solid #2A2E39;'>
        <br><h3 style='color: #E2E8F0; font-size:18px;'>📈 Nifty 50 Real-Time Chart Canvas</h3>
    <div class="tradingview-widget-container" style="height:350px;">
      <div id="tradingview_nifty" style="height:350px;"></div>
      <script type="text/javascript" src="https://tradingview.com"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "NSE:NIFTY", "interval": "15",
        "timezone": "Asia/Kolkata", "theme": "dark", "style": "1",
        "locale": "en", "toolbar_bg": "#131722", "enable_publishing": false,
        "hide_side_toolbar": false, "allow_symbol_change": true,
        "container_id": "tradingview_nifty"
      });
      </script>
    </div>
    """ , unsafe_allow_html=True)
        # --- ⚡ એડવાન્સ DIAGNA MULTI-KEYWORD & COMPLEX VOICE PROCESSOR ---
    st.markdown("<br><h3 style='color: #00F0FF; font-size:18px;'>🎙️ DIAGNA AI સ્માર્ટ આસિસ્ટન્ટ (મલ્ટિપલ એનાલિસિસ)</h3>", unsafe_allow_html=True)
    
    user_question = st.text_input("અહીં સવાલ લખો અથવા કીબોર્ડનું માઈક દબાવીને બોલો:", placeholder="દા.ત. નિફ્ટીનો ટ્રેન્ડ શું છે અને મારો સ્ટોપલોસ ક્યાં રાખવો?")

    if user_question:
        st.info("⚡ DIAGNA AI જટિલ સવાલનું એનાલિસિસ કરી રહ્યું છે...")
        
        q_low = user_question.lower()
        response_segments = []
        
        # ૧. મલ્ટિપલ કીવર્ડ એનાલિસિસ સેગમેન્ટ્સ
        if "ટ્રેન્ડ" in q_low or "માર્કેટ" in q_low or "trend" in q_low:
            response_segments.append(f"નિફ્ટી ૫૦ નો મુખ્ય ટ્રેન્ડ અત્યારે {trend_status} છે.")
            
        if "પ્રાઈઝ" in q_low or "ભાવ" in q_low or "price" in q_low or "કિંમત" in q_low:
            response_segments.append(f"નિફ્ટીની લાઈવ સ્પોટ કિંમત ₹{current_price:.2f} પર ટ્રેડ થઈ રહી છે જે આગલા બંધથી {price_change:.2f} પોઈન્ટ બદલાઈ છે.")
            
        if "સ્ટોપલોસ" in q_low or "ટાર્ગેટ" in q_low or "sl" in q_low:
            response_segments.append(f"આજના માર્કેટની વોલેટિલિટી મુજબ સેફ સ્ટોપલોસ {dynamic_sl} પોઈન્ટ અને પ્રોફિટ ટાર્ગેટ ₹{dynamic_target} રાખવો યોગ્ય રહેશે.")
            
        if "લોટ" in q_low or "ક્વોન્ટિટી" in q_low or "lot" in q_low or "માત્રા" in q_low:
            # લાઈવ કેપિટલના આધારે લોટ સાઈઝનું કેલ્ક્યુલેશન
            nifty_lot_size = 75
            raw_qty = (capital * (risk_pct / 100.0)) / premium_sl_points
            calculated_lots = int(raw_qty / nifty_lot_size)
            response_segments.append(f"તમારી ₹{capital} કેપિટલ અને {risk_pct}% રિસ્ક પ્રોફાઈલ પ્રમાણે તમારે વધુમાં વધુ {calculated_lots} લોટમાં કામ કરવું જોઈએ.")
            
        if "લાયસન્સ" in q_low or "યુઝર" in q_low:
            response_segments.append(f"તમે અત્યારે એક્ટિવ લાયસન્સ યુઝર {st.session_state['current_user']} તરીકે લોગીન છો.")

        # ૨. જો કોઈ જનરલ કે અતિ જટિલ સવાલ પૂછવામાં આવે તો (Fall-back Intelligent Response)
        if not response_segments:
            ai_response_text = f"ડિશંતભાઈ, તમે પૂછેલો પ્રશ્ન ટ્રેડિંગ વ્યુ ચાર્ટ પર અત્યારે પ્રાઈઝ એક્શન અને કેન્ડલસ્ટિક પેટર્ન નવો સપોર્ટ બનાવી રહ્યું છે તે દર્શાવે છે. નિફ્ટી અત્યારે ₹{current_price:.2f} પર હોવાથી અને એકંદર માર્કેટ સેન્ટિメント {trend_status} હોવાથી ઉતાવળ કર્યા વગર સિસ્ટમના પ્રીમિયમ કેલ્ક્યુલેટર મુજબ જ સ્ટોપલોસ સાથે ટ્રેડ લેવો હિતાવહ છે."
        else:
            # બધા જ જવાબોને ભેગા કરીને એક મોટો પ્રોફેશનલ કમ્પ્લીટ આન્સર બનાવવો
            ai_response_text = f"નમસ્તે ડિશંતભાઈ! મેં તમારા જટિલ સવાલનું વિશ્લેષણ કર્યું છે. " + " ".join(response_segments) + " મની મેનેજમેન્ટનું ખાસ ધ્યાન રાખજો."

        st.success(f"🤖 DIAGNA AI કોમ્પ્લેક્સ જવાબ: {ai_response_text}")
        
        # ૩. ગુજરાતીમાં અવાજ (Voice) જનરેટ કરવાની પ્રોસેસ
        tts = gTTS(text=ai_response_text, lang='gu', slow=False)
        tts.save("response.mp3")
        
        # ઓટોમેટિક ઓડિયો પ્લે કરવાનો જુગાડ
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'<audio src="data:audio/mp3;base64,{audio_base64}" autoplay="autoplay">'
            st.markdown(audio_html, unsafe_allow_html=True)
        # --- 🎙️ DIAGNA GUJARATI VOICE AI ASSISTANT ---
            
        # ઓટોમેટિક ઓડિયો પ્લે કરવાનો જુગાડ
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'<audio src="data:audio/mp3;base64,{audio_base64}" autoplay="autoplay">'
            st.markdown(audio_html, unsafe_allow_html=True)
        
        
