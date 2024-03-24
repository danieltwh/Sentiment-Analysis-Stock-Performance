from ast import Raise
from urllib.request import Request
import uvicorn
from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np
import pandas as pd
import datetime
from typing import Union, List

import os

# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# import models, crud, schemas

from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

import schemas

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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

# Dependency
# Json serialiser default 
def default(obj):
    if isinstance(obj,(datetime.date, datetime.datetime)):
        return obj.isoformat()

def load_tokenizer_and_model(dir_path):
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(dir_path, "tokenizer"), local_files_only=True, use_fast=True)
    trained_finbert = AutoModelForSequenceClassification.from_pretrained(
        os.path.join(dir_path, "model"), local_files_only=True)
    return tokenizer, trained_finbert    

def normalize_and_tokenize(text, tokenizer):
    text = text.lower()
    text_df = pd.DataFrame({"text": [text]})
    text_dataset = Dataset.from_pandas(text_df)
    def tokenize(x): return tokenizer(
        x["text"], padding="max_length", truncation=True)
    tokenized_text = text_dataset.shuffle(seed=42).map(tokenize, batched=True)
    # tokenized_text = tokenizer(text)
    return tokenized_text

@app.get("/", include_in_schema= False)
async def home():
    return RedirectResponse(url="/redoc")

########################################
""" Pre-load Sentiment Model """
########################################
dir_path = "./models"

labels = {1: 'negative', 2: 'neutral', 0: 'positive'}
pred_labels = {1: -1.0, 2: 0.0, 0: 1.0}


tokenizer, trained_finbert = load_tokenizer_and_model(dir_path)
trained_model = Trainer(trained_finbert,
                tokenizer=tokenizer
                )

########################################
""" APIs for News """
########################################
@app.post("/news-sentiment", tags=["News Data"],
    responses = {
        **responses,
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "title": "Insurance giant Aon ended its link to Trump. It\\u2019s far from alone: Here are others who\\u2019ve cut financial ties.", 
                    }
                    }}, 
            "description": """Returns the stock news that was created"""
        }
    },
    response_model = schemas.NewsSentiment
)
async def get_stock_sentiment(news: schemas.NewsInput):
    print(news)
    if news.title is None:
        raise HTTPException(status_code=400, detail="Missing news title")
    elif type(news.title) != str:
        raise HTTPException(status_code=400, detail="News title is not string")
    
    try:
        tokenized_text = normalize_and_tokenize(news.title, tokenizer)

        output = trained_model.predict(
            test_dataset=tokenized_text
        )

        prediction = np.argmax(output.predictions, axis=-1)[0]
        # print("here", prediction)
        sentiment = pred_labels[prediction]
        sentiment_label = labels[prediction]
        time = datetime.datetime.now()
        # print("here3", time, prediction, sentiment_label)
        
    except:
        raise HTTPException(status_code=503, detail="Model prediction failed")
    
    try:
        news_sentiment = schemas.NewsSentiment(
            title = news.title,
            date = time,
            sentiment = sentiment,
            label = sentiment_label,
        )
        print(news_sentiment)
    except:
        raise HTTPException(status_code=503, detail="News Sentiment schema failed to create")

    try:
        return Response(content = json.dumps(dict(news_sentiment), default=str), media_type="application/json")
    except:
        raise HTTPException(status_code=503, detail="Error with serialising and responding with NewsSentiment schema")

    



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port= 5000, reload = True)