import pika
import json
import sys
import os
import time
import traceback

import argparse
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas


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

    db = next(get_db())

    no_weeks = 10 # past n weeks of data from today to be collected (need to be a sufficiently distant past)
    query_weeks = 4
    buffer_weeks = 2

    end_date = (datetime.today() - timedelta(weeks=no_weeks + query_weeks + buffer_weeks))
    # start_date = end_date - timedelta(weeks=4)

    end_date_str = end_date.strftime("%Y-%m-%d")
    # start_date_str = start_date.strftime("%Y-%m-%d")

    # print(end_date_str)

    result = db.query(models.News
    ).filter(models.News.date < end_date_str).delete()

    db.commit()

    if debug:
        print('Done')
        print(f"Deleted {result} rows before {end_date_str}")
        # print(f"Deleted {len(result)}")
        # print(result)
    

if __name__ == "__main__":
    '''
        parameters to be populated
    '''
    parser = argparse.ArgumentParser(
                        prog = 'Delete Old News',
                        description = 'Delete old news in postgres database',
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
    
