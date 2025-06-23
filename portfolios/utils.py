import yfinance as yf

def fetch_nav(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            print(f"[ERROR] No data returned for {symbol}")
            return None
        latest_close = hist['Close'].iloc[-1]
        print(f"[YF] {symbol} latest close: {latest_close}")
        return float(latest_close)
    except Exception as e:
        print(f"[YF ERROR] Failed to fetch NAV for {symbol}: {e}")
        return None
