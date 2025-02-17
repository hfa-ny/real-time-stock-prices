import yfinance as yf
import streamlit as st
import pandas as pd
import time
import mplfinance as mpf  # Import mplfinance

st.title('Real-time Stock Price Visualization')

# User Input
ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, GOOG):", "AAPL").upper()
update_interval = st.slider("Update Interval (seconds)", 1, 60, 5)
period = st.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=0)
interval = st.selectbox("Data Interval", ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"], index=0)

# Caching Function
@st.cache_data(ttl=60)
def fetch_data(ticker_symbol, period_val, interval_val):
    try:
        ticker_data = yf.Ticker(ticker_symbol)
        data = ticker_data.history(period=period_val, interval=interval_val)
        return data, ticker_data.info.get("longName", ticker_symbol)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(), ""

# Initial Data Fetch
df, stock_name = fetch_data(ticker_symbol, period, interval)
if df.empty:
    st.error(f"Error fetching data for {ticker_symbol}")
    st.stop()


# --- Main Loop and Plotting ---
price_chart = st.empty()  # Placeholder for the chart

# Stop Button
if 'running' not in st.session_state:
    st.session_state['running'] = True
if st.button("Stop/Start Updates"):
    st.session_state['running'] = not st.session_state['running']

last_fetch_time = 0

while st.session_state['running']:
    current_time = time.time()
    if current_time - last_fetch_time >= update_interval:
        try:
            new_df, stock_name = fetch_data(ticker_symbol, period, interval)

            if not new_df.empty:
                df = new_df

                # --- Candlestick Plotting with mplfinance ---
                fig, ax = mpf.plot(
                    df,
                    type='candle',  # Specify candlestick chart
                    style='charles',  # Choose a style (optional)
                    title=f'{stock_name} ({ticker_symbol}) - {period}',
                    ylabel='Price (USD)',
                    volume=False,  # Show volume bars (optional)
                    returnfig=True,  # Return the figure and axes
                    show_nontrading=False # Hides non-trading days
                )

                price_chart.pyplot(fig)  # Display the figure
                last_fetch_time = current_time

        except Exception as e:
            st.error(f"An error occurred during data update: {e}")
            break

    time.sleep(1)

st.write("Updates stopped. Press Ctrl+C in your terminal to fully stop the script.")