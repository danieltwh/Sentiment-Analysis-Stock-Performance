from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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
    db_news = models.News(
        title = news.title,
        date = news.date,
        source = news.source,
        url = news.url,
        sentiment = news.sentiment,
        )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

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

def get_stock_sentiment(db: Session, stock_ticker: str):
    result = db.query(func.avg(models.StockNews.sentiment)).join(
    models.News, models.StockNews.news_id == models.News.id, isouter=True
    ).filter(models.StockNews.stock_ticker == stock_ticker).first()[0]
    return result
