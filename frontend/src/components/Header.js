import React from 'react'

function Header() {
  return (
    <div style={{marginTop: '10%', marginBottom: '5%'}}>
        <h2 className="text-center text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-500">
            Stock Sentiment API 
        </h2>
        <h4 className="text-center font-thin text-lg mt-2 text-slate-300">
          Get current stock news from various sources, along with NUS Fintech's sentiment rating. 
        </h4>
    </div>
  )
}


export default Header