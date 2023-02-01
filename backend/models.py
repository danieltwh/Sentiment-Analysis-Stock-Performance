from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    ticker = Column(String, primary_key = True, index = True)
    name = Column(String, unique = True, index = True)
    market_cap = Column(Float)
    country = Column(String)
    sector = Column(String)
    industry = Column(String)

    def __str__(self) -> str:
        return f"{self.ticker} {self.name}"

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    title = Column(String, index = True)
    date = Column(DateTime(timezone=True), server_default = func.now())
    source = Column(String)
    url = Column(String)
    # sentiment = Column(Float)
    # match = Column(Float)

    def __str__(self) -> str:
        return f"{self.id} {self.title} {self.date}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StockNews(Base):
    __tablename__ = "stocknews"

    stock_ticker = Column(String, ForeignKey("stocks.ticker"), primary_key = True, index = True)
    news_id = Column(Integer, ForeignKey("news.id"), primary_key = True, index = True)
    sentiment = Column(Float)
    match_score = Column(Float)

    def __str__(self) -> str:
        return f"{self.stock_ticker} {self.news_id} {self.sentiment} {self.match}"