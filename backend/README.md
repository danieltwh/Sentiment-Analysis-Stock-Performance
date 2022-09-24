# Sentiment-Analysis-Stock-Performance

## Table of Contents

- [Fintech Society ML - Open Banking](#fintech-society-ml---open-banking)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Requirements](#Requirements)
  - [Project Structure](#project-structure)
  - [Notes](#notes)
  - [Installation](#installation)
  - [Usage](#usage)

## Backend Overview
This folder houses the backend for the NUS FinTech Sentiment Analysis for Stock Performance project. It consists of xxx. This project was developed using FastAPI, PostgreSQL and Heroku. The deployed live link for the API: [API Link](https://nlp-stock-performance-backend.herokuapp.com/)

## Requirements
1. PostgreSQL installed in your system
2. gcloud/Heroku CLI installed in your system
3. Anaconda installed in your system
4. Docker installed in your system

## Notes

1. Model weights:
   Model weights are placed in the `weights` folder


## Installation

1. XXXX
    
    ```bash
    xxxxx
    ```
    
2. xxxxx
    
    ```bash
    xxxxx
    ``` 
   
3. xxxxxx

    ```bash
    python3 app.py
    ```

## Exposed APIs
The following APIs are exposed to interact with the database for the project. The deployed base live link for the API:
[API Link](https://nlp-stock-performance-backend.herokuapp.com/)

### Adding news data
A `POST` request has to be made to (link) with the content in JSON format.

| Attribute  | Example | Required |
| ------------- | ------------- |--|
| "token"  | `api access secret`  | yes|
| "date"  | "2023-01-02" | yes |
| "stock-ticker"  | "2023-01-02" | yes |
| "headline"  | "xxxx" | yes |
| "link"  | "https://www.xxx.com" | yes |
| "sentiment"  | "0.0" | yes |

Example of JSON body of POST request:

```
{
    "secret": "auth secret here",
    "date": "2023-01-02",
    "stock-ticker": "APPL",
    "headline": "xxx",
    "link": "https://www.BBC.com",
    "sentiment": "0.0",
}
```






