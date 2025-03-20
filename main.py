import yfinance as yf 

tsla = yf.Ticker("TSLA")
tsla_history= tsla.history(period="6mo")
print(tsla_history)