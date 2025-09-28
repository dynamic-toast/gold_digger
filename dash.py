import streamlit as st
from streamlit_autorefresh import st_autorefresh
import dash_func as func

st_autorefresh(interval=1000, key="refresh_chart")

st.set_page_config(page_title="Gold Digger V1.2 Dashboard", layout="wide")

# Init
if "jwt" not in st.session_state:
    st.session_state.jwt = None

if "data_stream" not in st.session_state:
    st.session_state.data_stream = False


# Ask user to login
if st.session_state.jwt is None:
    st.title(" Gold Digger V1.2 Login")

    # Present user with login form.
    with st.form("login_form"):
            email = st.text_input("📧 Email")
            api_key = st.text_input("🔑 API Key", type="password")
            submit = st.form_submit_button("Login")

    # If user submits
    if submit:
        try:
            # Login to dashboard using user input
            jwt = func.login(email, api_key)
            st.session_state.jwt = jwt
            st.success("✅ Login successful!")

            # Activate data stream
            if st.session_state.data_stream == False:
                from stream import StreamHandler
                bot = StreamHandler(st.session_state.jwt)
                bot.connect()
                print("LOG: Data stream connected -------")
                st.session_state.live_data = True
                
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

else: #If jwt token is present/User logged in ------- get account data.

    st.title("⛏️ Gold Digger V1.2 Dashboard")

    accounts = func.get_accounts(st.session_state.jwt)
    active_accounts = [a for a in accounts if a.get("canTrade", False)]

    df = func.load_bars()

    if active_accounts:
        account_names = [f"{a['name']} (ID: {a['id']})" for a in active_accounts]

        choice = st.selectbox("Available Accounts", account_names)
        selected_account = active_accounts[account_names.index(choice)]
        account_id = selected_account["id"]

        positions = func.search_positions(st.session_state.jwt, account_id)

        last_price = func.get_tick_price()
        if not last_price:
            pass

        open_pnl = func.compute_openpnl(positions, last_price)


        col1, col2 = st.columns([1, 1], gap=None, border=True, width="stretch", vertical_alignment="center")

        with col1:
            st.metric("Balance", f"${selected_account['balance']:.2f}")

        with col2:
            st.metric("Active Position", f"${open_pnl}")


        col1, col2 = st.columns([1, 1], gap=None, border=True, width="stretch", vertical_alignment="center")

        if "bot_states" not in st.session_state:
            st.session_state.bot_states = {}
        if "bot_start_times" not in st.session_state:
            st.session_state.bot_start_times = {}

        # Initialize this account's state if not present
        if account_id not in st.session_state.bot_states:
            st.session_state.bot_states[account_id] = False

        if account_id not in st.session_state.bot_start_times:
            st.session_state.bot_start_times[account_id] = None

        with col1:
            st.subheader("Bot Status:")

            if st.session_state.bot_states[account_id] == True:
                st.markdown(f"✅ Bot Status: Activated for ID: {account_id}")

                signal = func.activate_bot()
                import orders as od
                close = df["close"].iloc[-1]

                if signal == "INSUFFICIENT DATA":
                    print("LOG: Signal: ------- Insufficient Data")

                if signal["side"] == "HOLD":
                    print(f"LOG: Signal ------- {signal}")
                    
                if signal["side"] == "BUY":
                    print(f"LOG: Signal ------- {signal}")

                    positions = func.search_positions(st.session_state.jwt, account_id)
                    if positions:
                        print("LOG: Aleady in position ------- buy order rejected")
                    if not positions or len(positions) == 0:
                        order_note = od.long_order(st.session_state.jwt, account_id)
                        print("LOG: Order Note ------- ", order_note)


                    
                elif signal["side"] == "SELL":
                    print(f"LOG: Signal ------- {signal}")

                    positions = func.search_positions(st.session_state.jwt, account_id)
                    if positions:
                        print("LOG: Aleady in position ------- sell order rejected")
                    if not positions or len(positions) == 0:
                        order_note = od.short_order(st.session_state.jwt, account_id)
                        print("LOG: Order Note ------- ", order_note)

                # Deactivate button, when bot is active
                if st.button("Deactivate Bot"):
                    st.session_state.bot_states[account_id] = False
                    print("LOG: BOT DEACTIVATED -------")

            if st.session_state.bot_states[account_id] == False:
                st.markdown(f"❌ Bot Status: Deactivated for ID: {account_id}")

                # Activate button, when bot is deactivated
                if st.button("Activate Bot"):
                    st.session_state.bot_states[account_id] = True
                    print("LOG: BOT ACTIVATED -------")
        
        with col2:
            st.subheader("Controls:")
            col1, col2, col3 = st.columns([1, 1, 1], gap=None, border=True, width="stretch", vertical_alignment="center")
            import orders as od
            with col1:
                if st.button("Flatten"):
                    response = od.flatten(st.session_state.jwt, account_id)
                   
            with col2:
                if st.button("Buy Market"):
                    response = od.buy_market(st.session_state.jwt, account_id)
                    
            with col3:
                if st.button("Sell Market"):
                    response = od.sell_market(st.session_state.jwt, account_id)


        col1, col2 = st.columns([1, 1], gap=None, border=True, width="stretch", vertical_alignment="top")
                    
        with col1:
            col3, col4 = st.columns([1, 1], gap=None, width="stretch", vertical_alignment="center")
            with col3:
                st.header("GC (Gold Futures)")
            with col4:
                st.metric("Last Price: ", last_price)

        import pandas as pd
        trades = pd.read_csv("ticks.csv").tail(10)
        with col2:
            tick_stream = trades[["contract_id", "price", "volume", "timestamp"]]
            st.dataframe(tick_stream)



    else:
        print("LOG: ERROR: ------- No account data")
        st.rerun()
