import pika
import json
import sys
import os
import time
import traceback

import argparse

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

url = 'amqps://fzsatlsi:X6HeAHLC1mKDr2FZvSNIAWF9vg03riEs@woodpecker.rmq.cloudamqp.com/fzsatlsi'
port = 	5672
vhost = 'fzsatlsi'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main(debug = False):
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host = "localhost")
    # )

    connection = pika.BlockingConnection(
        # pika.ConnectionParameters(url=url, port=port, vhost=vhost)
        pika.URLParameters(url)
    )


    channel = connection.channel()
    channel.exchange_declare(
        exchange = "nlp_pred",
        exchange_type = "direct"
    )
    channel.queue_declare(queue = "raw_news", durable = True)
    channel.basic_qos(prefetch_count = 1)

    method_frame,  header_frame, body = channel.basic_get(queue = "raw_news")

    db = next(get_db())

    while method_frame != None and method_frame.NAME == "Basic.GetOk":
        
        try:
            raw_news = json.loads(body)

            if debug:
                print(f"""################
                    Recevied Message: {raw_news}
                    ################
                    """)

            # stock_ticker = raw_news['stock_ticker']
            # stock = crud.get_stock(db, stock_ticker)
            # if stock is None:
            #     crud.create_stock(stock_ticker)

            news_data = schemas.StockNewsCreate(
                title = raw_news['title'],
                date = raw_news['date'],
                source = raw_news['source'],
                url = raw_news['url'],
                sentiment = raw_news['sentiment'],
                match_score = raw_news['match_score'],
                stock_ticker = raw_news['stock_ticker'],
            )
            db_news, db_stock_news = crud.create_stock_news(db, news_data)
            
            if db_news != None and db_stock_news != None:
                if debug:
                    print("Done")
                channel.basic_ack(delivery_tag = method_frame.delivery_tag)
            else: 
                if debug:
                    print('Failed')
            
        except Exception as e:
            # print(e)
            traceback.print_exc()
        finally:
            # time.sleep(5)
            method_frame,  header_frame, body = channel.basic_get(queue = "raw_news")    

    connection.close()

if __name__ == "__main__":
    '''
        parameters to be populated
    '''
    parser = argparse.ArgumentParser(
                        prog = 'Consume News',
                        description = 'Consume News in RabbitMQ to populate database',
                        epilog = 'Text at the bottom of help')
    # parser.add_argument("-d", "--debug", type=bool, default=False)
    parser.add_argument('-d','--debug', dest='debug',action='store_true')

    args = parser.parse_args()

    is_debug = args.debug

    # print(is_debug, type(is_debug))

    try:
        main(is_debug)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
