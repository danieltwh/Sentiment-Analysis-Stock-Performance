import requests
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# from config import ALPHA_VANTAGE_API_KEY
from mlconfig import ALPHA_VANTAGE_API_KEY

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

def load_tracker(tracker_filename):
    df_tracker = pd.read_csv(tracker_filename)
    return df_tracker

def get_target_stock_tickers(df_tracker, n = 5):
    target_idx = df_tracker[df_tracker["is_done"].isnull()].index[:n]
    stock_tickers = df_tracker.loc[target_idx,]
    return stock_tickers
    # return list(zip(target_idx, stock_tickers))
    

def start_collection(tracker_filename =  "AlphaVantage_tracker.csv", 
prev_df_filename = "stock_news_daniel_v1", log_filename = "AlphaVantage_log.txt", n = 5):
    df_tracker = load_tracker(tracker_filename)
    stock_tickers = get_target_stock_tickers(df_tracker, n = n)
    
    collected_data = []
    log = open("AlphaVantage_log.txt", mode= "a")
    curr_time = pd.to_datetime(time.ctime())
    status = "FAIL"
    
    try:
        to_update = []

        failed_fetch = []
        
        stocks_no_news = []

        for idx, stock_ticker in stock_tickers.iterrows():
            payload = {
                "function": "NEWS_SENTIMENT",
                "tickers": stock_ticker["ticker"],
                "time_from" : stock_ticker["start_date"],
                "time_to" : stock_ticker["end_date"],
                "limit": 200,
                "apikey" : ALPHA_VANTAGE_API_KEY
            }
            # print(payload)
            
            resp = requests.get(ALPHA_VANTAGE_URL, params=payload)
            data = resp.json()

            try :
                # Fetch news data for the target stock ticker
                news = data["feed"]
                for news_data in news:
                    title = news_data["title"]

                    # Convert datetime to pandas datetime object
                    date_time = pd.to_datetime(news_data["time_published"]) 

                    source = news_data["source"]
                    url = news_data["url"]
                    summary = news_data["summary"]

                    sentiment_label = ""
                    for ticker_sentiment in news_data["ticker_sentiment"]:
                        if ticker_sentiment["ticker"] == stock_ticker:
                            sentiment_label = ticker_sentiment["ticker_sentiment_score"]

                    row = [title, date_time, source, url, summary, sentiment_label]

                    collected_data.append(row)
                to_update.append((idx, stock_ticker))
            except:
                # Log API error message
                # log.write(f"    {stock_ticker['ticker']}: {data}\n")
                failed_fetch.append((stock_ticker["ticker"], data))

                if "Information" in data and data["Information"] == "No articles found. Please adjust the time range or refer to the API documentation https://www.alphavantage.co/documentation#newsapi and try again.":
                    stocks_no_news.append((idx, stock_ticker))

        

        # Update data
        headers = [
            'title', "datetime", "source", "url", "summary", "sentiment_label"
        ]

        df_collected_news = pd.DataFrame(collected_data, columns = headers)
        prev_df = pd.read_csv(prev_df_filename)
        final_df = pd.concat([prev_df, df_collected_news], axis=0)

        final_df.to_csv(prev_df_filename, index=False)

        # Update df_tracker
        for idx, ticker in to_update:
            df_tracker.loc[idx, "is_done"] = True
        
        for idx, ticker in stocks_no_news:
            df_tracker.loc[idx, "is_done"] = True
        
        df_tracker.to_csv(tracker_filename, index=False)
        
        

        status = "SUCCESS"

        print(status)
    except:
        status = "FAIL"

    log.write(f"[{curr_time}] {status} Stock Tickers: {' '.join(list(stock_tickers['ticker']))}\n")
    for ticker, data in failed_fetch:
        log.write(f"    {ticker}: {data}\n")
    log.close()
    return 

if __name__ == '__main__':
    TRACKER_FILENAME =  "AlphaVantage_tracker.csv"
    PREV_DF_FILENAME = "stock_news_daniel_v1.csv"
    LOG_FILENAME = "AlphaVantage_log.txt"

    start_collection(TRACKER_FILENAME, PREV_DF_FILENAME, LOG_FILENAME, n = 2)
    