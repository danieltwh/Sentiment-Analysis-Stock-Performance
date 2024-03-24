from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

class News(BaseModel):
    title: str
    date: datetime
    # source: Optional[str] = None
    # url: Optional[str] = None
    # sentiment: float
    # match: float

    def __str__(self) -> str:
        return f"{self.date}: {self.title}"
    
class NewsSentiment(News):
    sentiment: float
    label: str
    # match: float

    def __str__(self) -> str:
        return f"{self.date} (Sentiment {self.sentiment}): {self.title}"

class NewsInput(BaseModel):
    title: str
    # source: Optional[str] = None
    # url: Optional[str] = None
    # sentiment: float
    # match: float

    def __str__(self) -> str:
        return f"{self.title}"


# class StockBase(BaseModel):
#     ticker: str
#     name: str
#     market_cap: float
#     country: str
#     sector: str
#     industry: str

#     def __str__(self) -> str:
#         return f"{self.ticker} {self.name}"

# class StockCreate(StockBase):
#     pass

# class Stock(StockBase):
#     class Config:
#         orm_mode = True



# class NewsBase(BaseModel):
#     title: str
#     date: datetime
#     source: Optional[str] = None
#     url: Optional[str] = None
#     # sentiment: float
#     # match: float

#     def __str__(self) -> str:
#         return f"{self.title} {self.date}"

# class NewsCreate(NewsBase):
#     pass

# class News(NewsBase):
#     id: int
#     class Config:
#         orm_mode = True
    
#     def __str__(self) -> str:
#         return f"{self.id}" + super().__str__()

# class StockNewsInput(NewsCreate):
#     # stock_ticker: str
#     sentiment: float
#     match_score: float

#     def __str__(self) -> str:
#         return  super().__str__() + f"{self.sentiment} {self.match_score}"

# class StockNewsCreate(StockNewsInput):
#     stock_ticker: str

#     def __str__(self) -> str:
#         return  super().__str__() + f"{self.sentiment} {self.match_score}"

# class StockNews(BaseModel):
#      stock_ticker: str
#      news_id: int
#      sentiment: float
#      match_score: Optional[float] = None

#      def __str__(self) -> str:
#         return  super().__str__() + f"{self.sentiment} {self.match_score}"



