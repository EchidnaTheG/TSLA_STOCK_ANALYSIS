import yfinance as yf 
import matplotlib.pyplot as plt
#We first import yfinance to get the data \n#! we will also now import matplotlib (this was added after doing data analisis)

#Here, we look for Tesla information and later get a history of the stock, we set the period to be 6mo
tsla = yf.Ticker("TSLA")
tsla_history= tsla.history(period="6mo")


# This shows the information of up to n number of rows at the head, aka the oldest ones to begin
def show_head_tsl(n):
    head_history_tsla= tsla_history.head(n)
    return head_history_tsla

#this checks if there is any missing values in the columns and sums it up
def check_missing_values():
    return tsla_history.isnull().sum()

#This gives a basic statistical summary for the stock
def show_basic_stats_tsl():
     basic_stats_tsla= tsla_history.describe()
     return basic_stats_tsla


#Here we call all the 3 functions in a single print() and the final output sort of looks like a report

print(f"{show_head_tsl(5)}\n{check_missing_values()}\n{show_basic_stats_tsl()}")

#Lets Try to plot the data, the X parameter axis will be the date, the Y parameter axis is the closing price
def access_closing_price_with_date(Ticker):
    closing_data = Ticker.Close
    time_data = Ticker.index
    plt.figure(figsize=(12, 6))  
    plt.plot(time_data, closing_data)
    plt.title('TSLA Stock Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.savefig('tesla_stock_plot.png')  # Save to file instead of showing
    plt.close()

access_closing_price_with_date(tsla_history)
