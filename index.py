import yfinance as yf
import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

st.title('Real-time Stock Price Visualization')

# Allow user to select the stock ticker
ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, GOOG):", "AAPL").upper()  # Default to AAPL

# --- Error Handling for Invalid Ticker ---
try:
    ticker_data = yf.Ticker(ticker_symbol)
    info = ticker_data.info  # Try to get info to check if ticker is valid
    stock_name = info.get("longName", ticker_symbol)  # Get company name, default to ticker
except Exception as e:
    st.error(f"Error fetching data for {ticker_symbol}: {e}")
    st.stop()  # Stop the app if the ticker is invalid

# --- User-Configurable Settings ---
update_interval = st.slider("Update Interval (seconds)", 1, 60, 5)  # Slider for update interval
period = st.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=0)  # Selectbox for period
interval = st.selectbox("Data Interval", ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"], index = 0) #select interval

# --- Caching Function ---
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_data(ticker, period_val, interval_val):
    """Fetches historical data and handles potential errors."""
    try:
        data = ticker.history(period=period_val, interval=interval_val)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# --- Initialize Data (using caching) ---
df = fetch_data(ticker_data, period, interval)
if df.empty:  # Check if the initial fetch failed
    st.stop()

# --- Main Loop ---
price_chart = st.empty()  # Placeholder for the chart
fig, ax = plt.subplots()

# --- Stop Button (using session_state) ---
if 'running' not in st.session_state: # Initialize if it's the program's first run
    st.session_state['running'] = True  # Initialize running state

if st.button("Stop/Start Updates"):
    st.session_state['running'] = not st.session_state['running'] # Change the running state

last_fetch_time = 0 # to prevent too frequent API calls.

while st.session_state['running']:
    current_time = time.time()
    if current_time - last_fetch_time >= update_interval:

        try:
            # --- Fetch only NEW data ---
            new_df = fetch_data(ticker_data, period, interval) # Fetch all. Better to combine with last data.
            
            if not new_df.empty:
                df = new_df # Replace the old dataframe with the new dataframe.
                
                prices = df['Close']

                # --- Plotting ---
                ax.clear()
                ax.plot(prices.index, prices.values)
                ax.set_xlabel('Time')
                ax.set_ylabel('Stock Price (USD)')
                ax.set_title(f'{stock_name} ({ticker_symbol}) Price - Period: {period}')
                ax.grid(True)
                fig.autofmt_xdate()

                price_chart.pyplot(fig)  # Update the chart
                last_fetch_time = current_time # Update to now.

        except Exception as e:
            st.error(f"An error occurred during data update: {e}")
            break # Stop updates on persistent error

    time.sleep(1) # Check every second if needs to be updated.

st.write("Updates stopped. Press Ctrl+C in your terminal to fully stop the script.") # Inform the user