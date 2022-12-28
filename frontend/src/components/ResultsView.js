import React, {useEffect, useState} from 'react'
import styled from 'styled-components';
import { Pagination, Stack } from '@mui/material';

function ResultsView(props) {
  const [results, setResults] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  // For pagination
  const [currPage, setCurrPage] = useState(1);
  const [numPages, setNumPages] = useState(1);
  const [recordsPerPage] = useState(5);
  const [displayedRecords, setDisplayedRecords] = useState([]);

// For updating results
  useEffect(() => {
    async function getStockData(ticker) {
      var tickerNews = [];
      let rawNewsData = await fetch(`https://nlp-stock-performance-backend.herokuapp.com/stock-news/${ticker}`)
        .then(res => res.text())
        .then(rawData => rawData.replaceAll("NaN", "null"));
      
      let stockSentiment = await fetch(`https://nlp-stock-performance-backend.herokuapp.com/stock-sentiment/${ticker}`)
        .then(res => res.json())
        .then(data => data.sentiment);

      const newsData = JSON.parse(rawNewsData).news;
      newsData.map(news => {
        news.ticker = ticker;
        tickerNews.push(news);
      });
      setSentiment(stockSentiment);
      setResults(tickerNews);
      const idxLastRecord = currPage * recordsPerPage;
      const idxFirstRecord = idxLastRecord - recordsPerPage;
      const currRecords = tickerNews.slice(idxFirstRecord, idxLastRecord);
      setDisplayedRecords(currRecords);
      const numPages = Math.ceil(tickerNews.length / recordsPerPage);
      setNumPages(numPages);
    }

    if (props.selectedTicker) {
        getStockData(props.selectedTicker);
    }
  }, [props.selectedTicker])


  const handlePaginationChange = (event, value) => {
    setCurrPage(value);
    const idxLastRecord = value * recordsPerPage;
    const idxFirstRecord = idxLastRecord - recordsPerPage;

    const currRecords = results.slice(idxFirstRecord, idxLastRecord);
    setDisplayedRecords(currRecords);
  }
  return (
    <div className="mt-8">
    <div className="mb-8">
      <h3 className="text-2xl font-thin text-center bg-sky-800/50 w-1/2 mx-auto py-2 px-1 rounded-full">Overall Sentiment: <span className="font-bold">{sentiment ? Math.round(sentiment * 1000) / 1000 : "NULL"}</span></h3>
    </div>
    {
      results.length > 0 ?
      <h2 class="text-2xl font-extrabold text-slate-300">LATEST NEWS</h2> :
      <></>
    }
    
    {
      displayedRecords.map((news) => ( // shuffles the array first
        <StockView> 
          <div className="flex justify-between">
            <a href={news.url} target="_blank" className="truncate text-sky-500 text-base hover:text-sky-700">{news.title}</a>
            <p className="text-xs font-bold text-sky-200 bg-sky-800/75 px-1.5 pt-1.5 pb-1 rounded">{news.sentiment ? Math.round(news.sentiment * 1000)/1000 : "NULL"}</p>
          </div>
          <span className="text-slate-300/75 text-sm">{news.date} | {news.source}</span>
        </StockView>
      ))
    }
    {
      results.length > 0 ?
      <Stack alignItems="center">
      <Pagination count={numPages} color="primary" page={currPage} onChange={handlePaginationChange} />
      </Stack> :
      <></>

    }
    </div>
  );
}

const StockView = styled.div `
min-height: 70px;
margin-left: auto;
margin-right: auto;
margin-top: 2%;
margin-bottom: 2%;
border-bottom: 1px solid rgba(255, 255, 255, 0.2);
`

export default ResultsView