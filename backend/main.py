from ast import Raise
from urllib.request import Request
import uvicorn
from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.responses import RedirectResponse
import json
import datetime
from typing import Union, List

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas


responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

description = """
## Objective
This project aims to explore NLP models, such as BERT (BERT-base, FinBERT), 
in predicting stock performance over a short-medium term time period (e.g. 1 year or less).

## Team Members
- Brandon Chiu
- Chan Zhuo Yang
- Daniel Tan
- Hans Neddyanto Tandjung
- Kleon Ang
- Teo Wei Ming
- Zheng Yilin

## About The Project
xxxx

"""

tags_metadata = [
    {
        "name": "Stock Data",
        "description": """Get all the financial information of stocks that are Mid-Cap or larger."""
    },
    {
        "name": "Market News",
        "description": """Get all the latest financial news filter by stock tickers"""
    },
]

swagger_ui_parameters = {
    "defaultModelsExpandDepth": -1,
}

app = FastAPI(
    title = "NLP for Stock Performance Prediction", 
    description = description,
    tags_metadata = tags_metadata,
    swagger_ui_parameters= swagger_ui_parameters
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Json serialiser default 
def default(obj):
    if isinstance(obj,(datetime.date, datetime.datetime)):
        return obj.isoformat()

@app.get("/", include_in_schema= False)
async def home():
    return RedirectResponse(url="/redoc")

########################################
""" APIs for Stock Data """
########################################
@app.get("/stock-tickers-list", response_model = List[str],tags=["Stock Data"],
    responses = {
        **responses,
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "stock-tickers": ["AAPL","AAWW","AB","ABB","ABBV","ABC","ABCB"]
                    }
                    }}, 
            "description": """Returns the list of stocker tickers that 
            users select for more information"""
        }
    }
)
async def get_all_stock_tickers(db: Session = Depends(get_db)):
    all_stocks = crud.get_all_stock_tickers(db)
    tickers = list(map(lambda x: x[0], all_stocks))
    result = {
        "stock-tickers": tickers
    }
    # return all_stocks
    return Response(content = json.dumps(result), media_type = "application/json")


########################################
""" APIs for News """
########################################
@app.get("/stock-news/{stock_ticker}", tags=["News Data"],
    responses = {
        **responses,
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "news": [
                            {"id": 33, "title": "Insurance giant Aon ended its link to Trump. It\\u2019s far from alone: Here are others who\\u2019ve cut financial ties.", "date": "2021-01-14T21:40:05", "source": "app.buzzsumo.com", "url": "https://www.chicagotribune.com/business/ct-biz-trump-capitol-aon-companies-drop-20210114-ykvz7gy33vhqxmgxhkrkgwtr2m-story.html", "sentiment": -0.37495, "match_score": 23.347578}, 
                            {"id": 34, "title": "All the businesses cutting ties with the Trump Organization", "date": "2021-01-14T20:12:36", "source": "businessinsider.com", "url": "https://www.businessinsider.com/all-the-businesses-cutting-ties-with-the-trump-organization-2021-1", "sentiment": -0.51555, "match_score": 26.602243}, 
                            {"id": 35, "title": "Juli\\u00e1n de la Cuesta se une a Allfunds como especialista de producto para Iberia y Am\\u00e9ricas", "date": "2021-01-14T19:46:18", "source": "fundssociety.com", "url": "https://www.fundssociety.com/es/noticias/nombramientos/julian-de-la-cuesta-se-une-a-allfunds-como-especialista-de-producto-para-iberia-y-americas", "sentiment": 0.0, "match_score": 24.955256}]
                    }
                    }}, 
            "description": """Returns the list of news that is relevant to the stock"""
        }
    }
)
async def get_stock_news(stock_ticker: str, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_ticker)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock ticker not found")
    news = crud.get_stock_news(db, stock_ticker)
    result = {}
    result["news"] = news
    return Response(content = json.dumps(result, default=str), media_type="application/json")

@app.get("/stock-sentiment/{stock_ticker}", tags=["News Data"],
    responses = {
        **responses,
        200: {
            "content": {
                "application/json": {
                    "example": {
                        'sentiment': 0.41823
                        }
                    }}, 
            "description": """Returns current news sentiment of the stock"""
        }
    }
)
async def get_stock_sentiment(stock_ticker: str, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_ticker)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock ticker not found")
    sentiment = crud.get_stock_sentiment(db, stock_ticker)
    if sentiment is None:
        raise HTTPException(status_code=404, detail="No sentiment not found")
    result = {}
    result["sentiment"] = sentiment
    return Response(content = json.dumps(result, default=str), media_type="application/json")

@app.get("/news/{news_id}", response_model = schemas.News, tags=["News Data"],
    responses = {
        **responses,
        200: {
            "content": {
                "application/json": {
                    "example": {
                        # "stock-tickers": ["AAPL","AAWW","AB","ABB","ABBV","ABC","ABCB"]
                    }
                    }}, 
            "description": """Returns the list of stocker tickers that 
            users select for more information"""
        }
    }
)
async def get_news_by_ID(news_id: int, db: Session = Depends(get_db)):
    news_data = crud.get_news(db, news_id)
    if news_data is None:
        raise HTTPException(status_code=404, detail="News ID not found")
    return news_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port= 5000, reload = True)