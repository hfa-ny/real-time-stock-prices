import yfinance as yf
import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

st.title('Real-time Stock Price Visualization')

# Allow user to select the stock ticker
ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, GOOG):", "AAPL").upper()  # Default to AAPL

# --- User-Configurable Settings ---
update_interval = st.slider("Update Interval (seconds)", 1, 60, 5)
period = st.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=0)
interval = st.selectbox("Data Interval", ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"], index = 0)

# --- Caching Function ---
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_data(ticker_symbol, period_val, interval_val): #<-- Pass string, not object.
    """Fetches historical data and handles potential errors."""
    try:
        ticker_data = yf.Ticker(ticker_symbol) # Create Ticker object *inside* the cached function
        data = ticker_data.history(period=period_val, interval=interval_val)
        return data, ticker_data.info.get("longName", ticker_symbol) # Return both data and name.
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(), ""  # Return empty DataFrame and name on error


# --- Initialize Data (using caching) ---
df, stock_name = fetch_data(ticker_symbol, period, interval)  #<-- Pass the string!
if df.empty:
    st.error(f"Error fetching data for {ticker_symbol}") # error when it is invalid
    st.stop()



# --- Main Loop ---
price_chart = st.empty()
fig, ax = plt.subplots()

# --- Stop Button (using session_state) ---
if 'running' not in st.session_state:
    st.session_state['running'] = True

if st.button("Stop/Start Updates"):
    st.session_state['running'] = not st.session_state['running']

last_fetch_time = 0

while st.session_state['running']:
    current_time = time.time()
    if current_time - last_fetch_time >= update_interval:

        try:
            # --- Fetch only NEW data ---
            new_df, stock_name = fetch_data(ticker_symbol, period, interval)  # Fetch all. Better to combine with last data.

            if not new_df.empty:
                df = new_df
                prices = df['Close']

                # --- Plotting ---
                ax.clear()
                ax.plot(prices.index, prices.values)
                ax.set_xlabel('Time')
                ax.set_ylabel('Stock Price (USD)')
                ax.set_title(f'{stock_name} ({ticker_symbol}) Price - Period: {period}')
                ax.grid(True)
                fig.autofmt_xdate()

                price_chart.pyplot(fig)
                last_fetch_time = current_time

        except Exception as e:
            st.error(f"An error occurred during data update: {e}")
            break # Stop updates on persistant error

    time.sleep(1)

st.write("Updates stopped. Press Ctrl+C in your terminal to fully stop the script.")