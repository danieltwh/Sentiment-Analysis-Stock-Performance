from fastapi import Response
from pydantic import BaseModel

from typing import List

# GET /stock-tickers-list
class StockTickersList_Response(BaseModel):
    stock_tickers : List[str] = []

