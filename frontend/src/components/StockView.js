import React, { useEffect, useState } from 'react';
import stocksData from '../nasdaq_stocks.json';
import axios from '../axios.js';
import Autocomplete from '@mui/material/Autocomplete';
import { TextField, makeStyles } from '@mui/material';
import ResultsView from './ResultsView';

function StockView() {
    const [tickers, setTickers] = useState([]);
    const [selectedTicker, setSelectedTicker] = useState('');

    useEffect(() => {
      async function getTickers() {
        let tickerData = await axios.get('stock-tickers-list').then(res => res['data']['stock-tickers']);
        setTickers(tickerData);
      }
      var dataTickers = stocksData.map(stockData => stockData.Symbol);
      getTickers();
      setTickers(dataTickers);
    }, [])
  return (
    <div className="w-3/5 mx-auto mb-8">
        <Autocomplete
        size="small"
        options={tickers}
        value={selectedTicker}
        onInputChange={(event, newInputValue) => {
          setSelectedTicker(newInputValue);
        }}
        filterSelectedOptions
        renderInput={(params) => (
            <TextField
              {...params}
              placeholder='Search a stock ticker...'
            />
          )}
        />
        <ResultsView selectedTicker={selectedTicker} />
    </div>
  )
}

export default StockView