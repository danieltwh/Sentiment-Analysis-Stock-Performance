import React from 'react';
import './App.css';
import Header from './components/Header'
import StockView from './components/StockView'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <div className="App">
        <Header />
        <StockView />
      </div>
    </ThemeProvider>
  );
}

export default App;
