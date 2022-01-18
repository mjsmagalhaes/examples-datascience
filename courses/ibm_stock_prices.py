import yfinance as yf

papers = ['GME', 'TSLA']
apple = yf.Ticker("AAPL")
apple.info['country']
apple_share_price_data = apple.history(period="max")
