import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
import json

with open("stock-tickers.txt", "r") as f:
    stock_tickers_list = f.read().split(",")
    stock_ticker_tracker = {val: val for val in stock_tickers_list}

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

app = FastAPI(
    title = "NLP for Stock Performance Prediction", 
    description = description,
    tags_metadata = tags_metadata
)

@app.get("/", include_in_schema= False)
async def home():
    return RedirectResponse(url="/docs")

@app.get("/stock-tickers-list", tags=["Stock Data"],
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
async def getAllStockTickers():

    data = {
        "stock-tickers": list(stock_ticker_tracker.keys())
    }

    return Response(content = json.dumps(data), media_type = "application/json")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port= 5000, reload = True)