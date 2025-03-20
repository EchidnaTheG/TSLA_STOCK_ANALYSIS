import yfinance as yf 
#We first import yfinance to get the data

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
