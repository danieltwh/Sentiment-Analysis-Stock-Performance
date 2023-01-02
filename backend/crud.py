from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import desc

import models
import schemas

def get_stock(db: Session, stock_ticker: str):
    return db.query(models.Stock).filter(models.Stock.ticker == stock_ticker).first()

def get_all_stocks(db: Session):
    return db.query(models.Stock).all()

def get_all_stock_tickers(db: Session):
    return db.query(models.Stock).with_entities(models.Stock.ticker).all()

def create_stock(db: Session, new_stock: schemas.StockCreate):
    db_stock = models.Stock(
        ticker = new_stock.ticker,
        name = new_stock.name,
        market_cap = new_stock.market_cap,
        country = new_stock.country,
        sector = new_stock.sector,
        industry = new_stock.industry
        )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def create_news(db: Session, news: schemas.NewsCreate):
    db_news = models.News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def delete_news(db: Session, news_id: int):
    db.query(models.News).filter(models.News.id == news_id).delete()
    db.commit()
    return


def get_stock_news(db: Session, stock_ticker: str):
    columns = [
        models.News.id,
        models.News.title,
        models.News.date,
        models.News.source,
        models.News.url,
        models.StockNews.sentiment,
        models.StockNews.match_score
        ]

    result = db.query(*columns).join(
    models.News, models.StockNews.news_id == models.News.id, isouter=True
        ).filter(models.StockNews.stock_ticker == stock_ticker).all()
    result = list(map(lambda x: dict(x), result))
    return result


# def create_stock_news(db: Session, news_data: schemas.NewsCreate, stock_news: schemas.StockNews,):
def create_stock_news(db: Session, stock_news_data: schemas.StockNewsCreate):
    # Creating the news model for inserting news data
    news_data = stock_news_data.dict()
    del news_data["sentiment"]
    del news_data["match_score"]
    del news_data["stock_ticker"]

    # Creating the news entry
    db_news = models.News(**news_data)
    db.add(db_news)
    db.flush()

    # Check if insertion of news entry was successful
    if db_news is None:
        db.rollback()
        return None, None

    # If successful, insert the new stock_news relationship
    db_stock_news = models.StockNews(
        stock_ticker = stock_news_data.stock_ticker,
        news_id = db_news.id,
        sentiment = stock_news_data.sentiment,
        match_score = stock_news_data.match_score
    )
    
    db.add(db_stock_news)
    db.flush()

    # Commit the new changes
    db.commit()
    return db_news, db_stock_news


def get_stock_sentiment(db: Session, stock_ticker: str):
    result = db.query(func.avg(models.StockNews.sentiment)).join(
    models.News, models.StockNews.news_id == models.News.id, isouter=True
    ).filter(models.StockNews.stock_ticker == stock_ticker).first()[0]
    return result

def get_last_news(db: Session, stock_ticker: str):
    columns = [
        models.News.id,
        models.News.title,
        models.News.date,
        models.News.source,
        models.News.url,
        models.StockNews.sentiment,
        models.StockNews.match_score
        ]

    result = db.query(*columns).join(
    models.News, models.StockNews.news_id == models.News.id, isouter=True
        ).filter(models.StockNews.stock_ticker == stock_ticker).order_by(desc(models.News.date)).first()
    if result == None:
        return {}
    else:
        result = dict(result)
        return result
