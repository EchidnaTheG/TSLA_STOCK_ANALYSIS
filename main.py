import yfinance as yf 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

#!!!print(f"{show_head_tsl(5)}\n{check_missing_values()}\n{show_basic_stats_tsl()}") #2 This was made into a comment since this is not needed at the moment

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

#!!!access_closing_price_with_date(tsla_history) #2 This was made into a comment since this was already plotted, no need to do it every runtime /n#3 In Order To standardize everything, the  SMA functions will use 1y 

def calculation_moving_averages_SMA_50(Ticker):
    if len(Ticker) >= 50:
        Ticker["SMA_50"] = Ticker.Close.rolling(window=50).mean()
        plt.figure(figsize=(12, 6))  
        plt.plot(Ticker.index, Ticker.SMA_50)
        plt.title(f'TSLA Stock SMA_50 Prices')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.savefig('tesla_stock_SMA_50_plot.png')  
        plt.close()
    else:
        raise ValueError("Not Enough Data for SMA_50")


#For this to work, we need TSLA data that goes further than 6 months, which is why another Ticker for TSLA will be created, 1year
tsla_history_1y= tsla.history(period="1y")
#We are calculating averages, something used as sell or buy signals, 50 is short, 200 is long

def calculation_moving_averages_SMA_200(Ticker):
    if len(Ticker) >= 200:
        Ticker["SMA_200"] = Ticker.Close.rolling(window=200).mean()
        plt.figure(figsize=(12, 6))  
        plt.plot(Ticker.index, Ticker.SMA_200)
        plt.title('TSLA Stock SMA_200 Prices')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.savefig('tesla_stock_SMA_200_plot.png')  
        plt.close()
    else:
        raise ValueError("Not Enough Data for SMA_200")
    
#!!!calculation_moving_averages_SMA_200(tsla_history_1y) #3 This was made into a comment since this was already plotted
#!!!calculation_moving_averages_SMA_50(tsla_history_1y) #3 This was made into a comment since this was already plotted
#Overalying all on a single plot
def overlaying_SMA(Ticker):
    if len(Ticker) >= 200:
        Ticker["SMA_50"] = Ticker.Close.rolling(window=50).mean()
        Ticker["SMA_200"] = Ticker.Close.rolling(window=200).mean()
        plt.figure(figsize=(12, 6))  
        plt.plot(Ticker.index, Ticker.SMA_50,label="50-Day SMA", color="blue")
        plt.plot(Ticker.index, Ticker.SMA_200, label="200-Day SMA", color="orange")
        plt.plot(Ticker.index, Ticker.Close,label="Closing Price", color="red")
        plt.title('TSLA Stock_Overlaying_SMA')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.savefig('tesla_stock_Overlaying_SMA_plot.png')  
        plt.close()
    else:
        raise ValueError("Not Enough Data for Overlaying_SMA")

#!!!overlaying_SMA(tsla_history_1y) #4 Done already! no need to repeat at runtime
#this calculates the average change everyday
def pct_change(Ticker):
    Ticker.Daily_Return= Ticker.Close.pct_change()
    plt.figure(figsize=(10, 6))
    sns.histplot(Ticker.Daily_Return.dropna(), bins=50, kde=True)
    plt.title('Daily Returns Distribution')
    plt.xlabel('Daily Returns')
    plt.ylabel('Frequency')
    plt.savefig('tesla_stock_PCT_CHANGE_plot.png')  
    plt.close()

#!!!pct_change(tsla_history_1y) #5 Done Already! No need to repeat at runtime
#This computes how volatile a stock is, the higher, the riskier but higher rewards and viceversa
def compute_volability(Ticker):
    Ticker.Daily_Return= Ticker.Close.pct_change()
    volatility = Ticker.Daily_Return.std()
    return volatility

#!!!print(f"TSLA Volatily {compute_volability(tsla_history_1y)}") #6 Done!
#this gives corrrel between two tickers
def compute_correl_two_Tickers_Daily_Return(Ticker1, Ticker2):
    Ticker1.Daily_Return= Ticker1.Close.pct_change()
    Ticker2.Daily_Return= Ticker2.Close.pct_change()
    correl_coefficient= Ticker1.Daily_Return.corr(Ticker2.Daily_Return)
    return correl_coefficient

aapl= yf.Ticker("AAPL")
aapl_history= aapl.history(period="1y")
correl=compute_correl_two_Tickers_Daily_Return(tsla_history_1y,aapl_history)


#calculalate correl for n number of tickers and make a heatmap of them

def correl_heatmap(*tickers):
    stock_data= {}
    for Ticker in tickers:
        stock= yf.Ticker(Ticker)
        stock_history= stock.history(period="1y")
        stock_history.Daily_Return= stock_history.Close.pct_change()
        stock_data[Ticker] = stock_history.Daily_Return
    final_df= pd.DataFrame(stock_data)
    correl_matrix= final_df.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correl_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Stock Correlation Heatmap")
    plt.savefig("correlation_heatmap.png")

#!!!correl_heatmap("TSLA", "AAPL", "MSFT", "NVDA") #7 Already Saved
#this computes the sharp ratio for an number of *args tickers, one key note is that a ticker such as "TSLA" is needed, not the history, 
#this codebase has made the error of using the terms interchangeably, note that here the function calcultes it, this will change later 
#For now, we are experimenting with stuff, later on, we will use the functions we have created and adapt where needed to see if we can make a cli tool or something..
def compute_sharp_ratio(*tickers):
    stock_data={}
    for ticker in tickers:
        stock= yf.Ticker(ticker)
        stock_history= stock.history(period="1y")
        stock_history.Daily_Return= stock_history.Close.pct_change()
        risk_free_sharp= (stock_history.Daily_Return.mean()-(0.03/252)) / (compute_volability(stock_history))
        stock_data[ticker]= risk_free_sharp
    return stock_data


def compute_rsi(ticker_hist):
    delta= ticker_hist.Close.diff()
    gain= delta.where(delta>0, 0)
    loss = -delta.where(delta<0,0)
    avg_gain = gain.rolling(window = 14, min_periods=1).mean()
    avg_loss = loss.rolling(window = 14, min_periods=1).mean()
    RS= avg_gain/avg_loss
    RSI= 100-(100/(1+RS))
    ticker_hist["RSI"] =RSI
    return ticker_hist["RSI"]


 