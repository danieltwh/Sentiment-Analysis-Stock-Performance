import pika

import models
import schemas
import crud
from database import SessionLocal, engine, SQLALCHEMY_DATABASE_URL

import argparse
import json
import os
import yaml
import io

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os.path
from datetime import datetime, timedelta
import datetime
import aiohttp
import asyncio


# get the range of stock tickers
def get_stock_tickers(start, end, df):
  return df.loc[start-1:end-1, "ticker"].to_numpy()

# parse news from dictionary into pd.DataFrame
def process_news_data(news_dict):
  df = pd.DataFrame()
  for ticker in news_dict:
    news = news_dict[ticker]
    title = list(map(lambda x: x['title'], news['data']))
    pub_date = list(map(lambda x: x['published_at'], news['data']))
    source = list(map(lambda x: x['source'], news['data']))
    url = list(map(lambda x: x['url'], news['data']))
    entities = list(map(lambda x: list(filter(lambda y: y['symbol'] == ticker, x['entities']))[0], news['data']))
    match_score = list(map(lambda x: x["match_score"], entities))
    sentiment_score = list(map(lambda x: x["sentiment_score"], entities))

    def process_text(text):
      text = text.replace('\n\n', '... ')
      text = BeautifulSoup(text, 'html.parser').get_text()
      return text
    text = list(map(lambda y: '\n'.join(list(map(lambda z: process_text(z['highlight']), y))), list(map(lambda x: x['highlights'], entities))))
    
    row = {
        "Stock": [ticker] * len(title), 
        "Title": title, 
        "Date/Time Published": pub_date, 
        "Source": source, 
        "Url": url,
        "Relevant Texts": text,
        "Sentiment Score": sentiment_score,
        "Match Score": match_score
        }
    temp = pd.DataFrame(row)
    df = df.append(temp, ignore_index = True)
  return df


# fetch news from one token
# async def fetch_token_news(session, token, start_idx, df):
#     tasks = []
#     for i in range(10):
#       s = start_idx + i * 10
#       e = s + 9
#       if i == 6: await asyncio.sleep(300)
#       try:
#         # tickers_set = get_stock_tickers(s, e, df) 
#         for idx in range(s, e + 1):
#           start_date = df.loc[idx, "start_date"].strftime("%Y-%m-%d")
#           end_date =min(start_date + datetime.timedelta(weeks=2), datetime.datetime.today()).strftime("%Y-%m-%d")
#           url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&api_token={token}&filter_entities=true&published_before={end_date}&published_after={start_date}"
#           async with session.get(url) as response:
#             tasks.append(await response.json())
#       except:
#         print(f"Fail at range {s} - {e}")
#     return tasks


async def fetch_token_news(session, token, start_idx, df, start_date):
    tasks = []
    # end_date = datetime.datetime.today().strftime("%Y-%m-%d")
    # target_date = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    counter = 0
    for i in range(10):
      s = start_idx + i * 10
      e = s + 9
      if counter == 6: 
        await asyncio.sleep(300)
        counter = 0
      try:
        tickers_set = get_stock_tickers(s, e, df) 
        print(tickers_set)
        counter += len(tickers_set)
        for ticker in tickers_set:
          # url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&api_token={token}&filter_entities=true&published_before={end_date}&published_after={start_date}"
          # url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&api_token={token}&filter_entities=true&published_before={target_date}"
          url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&api_token={token}&filter_entities=true&published_on={start_date}"
          async with session.get(url) as response:
            tasks.append(await response.json())
      except:
        print(f"Fail at range {s} - {e}")
    return tasks

# fetch news from all tokens asynchronously
# async def fetch_all_news_data_async(df):
#   news = {}
#   tasks = []
#   async with aiohttp.ClientSession() as session:
#     for idx in range(len(API_KEYS)):
#       token = API_KEYS[idx]
#       start_idx = start_indexes[idx]
#       tasks.append(fetch_token_news(session, token, start_idx, df))
#     responses = await asyncio.gather(*tasks)
#     for response in responses:
#       for result in response:
#         try:
#           ticker = result["data"][0]["entities"][0]["symbol"]
#           news[ticker] = result
#         except Exception as err:
#           print(f"Rate limit reached")
#   return news

async def fetch_all_news_data_async(df, start_date):
  news = {}
  tasks = []
  async with aiohttp.ClientSession() as session:
    for idx in range(len(API_KEYS)):
      token = API_KEYS[idx]
      start_idx = start_indexes[idx]
      tasks.append(fetch_token_news(session, token, start_idx, df, start_date))
      # tasks.append(fetch_token_news(session, token, start_idx, df))
    responses = await asyncio.gather(*tasks)
    print("here")
    for response in responses:
      for result in response:
        try:
          ticker = result["data"][0]["entities"][0]["symbol"]
          news[ticker] = result
        except Exception as err:
          print(f"Rate limit reached")
  return news

def get_request_param(APIS, stocks):
    request_param = []
    for idx, ticker in stocks:
        is_found = False
        param = {
            "idx": idx,
            "ticker": ticker
        }
        for api_key, api_param in APIS:
            # print(idx, api_param["start_index"],  api_param["end_index"])
            if api_param["start_index"] <= idx <= api_param["end_index"]:
                param["api_key_name"] = api_key
                param["api_key"] = api_param["key"]
                request_param.append(param)
                is_found = True
                break;
            elif api_param["start_index"] == "*" and api_param["end_index"] == "*":
                param["api_key_name"] = api_key
                param["api_key"] = api_param["key"]
                request_param.append(param)
                is_found = True
                break;
            elif api_param["start_index"] <= idx and api_param["end_index"] == "*":
                param["api_key_name"] = api_key
                param["api_key"] = api_param["key"]
                request_param.append(param)
                is_found = True
                break;
            elif api_param["start_index"] == "*" and idx <= api_param["end_index"] :
                param["api_key_name"] = api_key
                param["api_key"] = api_param["key"]
                request_param.append(param)
                is_found = True
                break;
        
        if not is_found:
            raise Exception(f"Failed to allocate API key for index {idx}: {ticker}")
    return request_param


if __name__ == "__main__":
  '''
    parameters to be populated
  '''
  parser = argparse.ArgumentParser(
                    prog = 'Fetch News',
                    description = 'Fetch news related to the stock tickers from Marketaux',
                    epilog = 'Text at the bottom of help')
  parser.add_argument("-s", "--start", type=int,required=True)
  parser.add_argument("-e", "--end", type=int, required=True)

  args = parser.parse_args()
  start_idx = args.start
  end_idx = args.end
  print(start_idx, end_idx)

  API_FILE = "api_tracker.yaml"
  with open(API_FILE) as f:
      generator = yaml.safe_load(f)
      APIS = list(generator)
      APIS = list(map(lambda x: tuple(x.items())[0], APIS))
  # for api in APIS[:2]:
  #     print(api)

  
  API_KEYS = [val["key"] for key, val in APIS] # pass in the list of API tokens
  start_indexes = [val["start_index"] for key, val in APIS] # pass in the list of start index corresponding to each API token
  # API_KEYS = ["uvi3iw3bL4jaROoaT0TGgbu0HRr9sQc9mWyMhFCa", "QAtmHlReb9ZdjaicSgdpARuHGYVYJgzjYuSiFXD7"]
  # start_indexes = [0, 100]
  no_weeks = 20 # past n weeks of data from today to be collected (need to be a sufficiently distant past)

  stocks = []
  try:
    db = SessionLocal()
    sql_query = f'''
      SELECT *
      FROM (SELECT ROW_NUMBER() OVER (ORDER BY ticker) as idx, ticker 
        FROM stocks) as t
      WHERE idx BETWEEN {start_idx} AND {end_idx};
    '''
    stocks = db.execute(sql_query).all()
    # request_param = get_request_param(APIS, stocks)
    # print("Length of request param:",len(request_param))
    # print(request_param[:2])
  finally:
    db.close()
  # print(stocks)
  df = pd.DataFrame(stocks, columns=["index", 'ticker']).set_index("index")
  # print(df)

  # df["start_date"] = np.nan
  # print(df.head(5))

  # try:
  #     db = SessionLocal()

  #     for idx in df.index:
  #       ticker = df.loc[idx, "ticker"]
  #       news = crud.get_last_news(db, ticker)
  #       if len(news) == 0:
  #         date = None
  #         start_date = (datetime.datetime.today() - timedelta(weeks=2)).replace(hour=0, minute=1, second=0)
  #       else:
  #         date = news["date"]
  #         # date.strftime("%Y-%m-%d")
  #         start_date = (date + timedelta(days=1)).replace(hour = 0, minute = 1, second = 0)
  #       print(ticker, date, start_date)
  #       df.loc[idx, "start_date"] = start_date  
  # finally:
  #   db.close()
  # print("Insert start dates")
  # print(df.head(5))

  start_date = (datetime.datetime.today() - timedelta(weeks=no_weeks)).strftime("%Y-%m-%d")

  news = asyncio.run(fetch_all_news_data_async(df, start_date))

  # news = asyncio.run(fetch_all_news_data_async(df))

  news_df = process_news_data(news)

  stock_news = []

  for idx, row in news_df.iterrows():
    curr_stock_news = dict(
      stock_ticker = row["Stock"],
      title = row["Title"],
      date = row["Date/Time Published"],
      source = row['Source'],
      url = row["Url"],
      sentiment = row["Sentiment Score"],
      match_score = row["Match Score"]
    )
    stock_news.append(curr_stock_news)
  
  # print(stock_news)

  url = 'amqps://fzsatlsi:X6HeAHLC1mKDr2FZvSNIAWF9vg03riEs@woodpecker.rmq.cloudamqp.com/fzsatlsi'
  port = 	5672
  vhost = 'fzsatlsi'


  # connection = pika.BlockingConnection(
  #         pika.ConnectionParameters(url=url, port=port, vhost=vhost)
  #     )

  connection = pika.BlockingConnection(
      pika.URLParameters(url)
  )

  channel = connection.channel()
  # q = channel.queue_bind(exchange="nlp_pred", queue="raw_news")
  # channel.basic_get(queue = "raw_news")
  channel.exchange_declare(
      exchange = "nlp_pred",
      exchange_type = "direct"
  )
  channel.queue_declare(queue = "raw_news", durable=True)
  # raw_news = {
  #     "title": "AMG to Announce …",
  #     "date": "2021-01-28 18:05:48",
  #     "source": "benzinga.com",
  #     "url": "https://www.benzinga.com/",
  #     "ticker": "AMG",
  #     # "sentiment": -0.37495,
  #     "match_score" : 23.347578
  # }
  # msg = json.dumps(raw_news)
  # msg

  for curr_news in stock_news:
    msg = json.dumps(curr_news)
    channel.basic_publish(
        # exchange = "nlp_pred",
        exchange = "",
        routing_key = "raw_news",
        body = msg,
        properties = pika.BasicProperties(
            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
  connection.close()

  



  # for idx, row in news_df.iterrows():
  #   stock_news = schemas.StockNewsCreate(
  #     stock_ticker = row["Stock"],
  #     title = row["Title"],
  #     date = row["Date/Time Published"]
  #     url = row["Url"],
  #     # sentiment = row["Sentiment Score"],
  #     match_score= = row["Match Score"]
  #   )





  # csv_name = f"test_data/marketaux_newsdata_async.csv"
  # filename = csv_name

  # if not os.path.exists(filename):
  #   news_df.to_csv(filename)
  # else:
  #   print("File already exists")







  # try:
  #   db = SessionLocal()

  #   for idx in range(len(request_param)):
  #     param = request_param[idx]
  #     news = crud.get_last_news(db, param["ticker"])
  #     if len(news) == 0:
  #       date = None
  #       start_date = datetime.datetime.today() - timedelta(weeks=2)
  #     else:
  #       date = news["date"]
  #       # date.strftime("%Y-%m-%d")
  #       start_date = (date + timedelta(days=1)).replace(hour = 0, minute = 1, second = 0)
  #     print(param["ticker"], date, start_date)
  #     param["start_date"] = start_date      
  # finally:
  #   db.close()
  # print("Insert start dates")
  # print(request_param[:2])




  # input_filename = "<absolute path of nasdaq_screener_csv>"
  # output_dirname = "<absolute path of the directory where you will be storing the collected data>"
  # API_KEYS = [] # pass in the list of API tokens
  # start_indexes = [] # pass in the list of start index corresponding to each API token
  # no_weeks = 20 # past n weeks of data from today to be collected (need to be a sufficiently distant past)
  
  # start_date = (datetime.today() - timedelta(weeks=no_weeks)).strftime("%Y-%m-%d")

  # df = pd.read_csv(input_filename)

  # news = asyncio.run(fetch_all_news_data_async(df, start_date))
  # news_df = process_news_data(news)

  # date = datetime.today().strftime("%Y-%m-%d")
  # csv_name = f"/marketaux_newsdata_async_{date}.csv"
  # filename = output_dirname + csv_name

  # if not os.path.exists(filename):
  #   news_df.to_csv(filename)
  # else:
  #   print("File already exists")




