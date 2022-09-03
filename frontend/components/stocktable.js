import { green } from '@mui/material/colors';
import React, { useState } from 'react';
import DataTable from 'react-data-table-component';



function CustomTable () {


  const columns = [

    {
      name: "Rank", 
      selector: row => row.ranking,
      conditionalCellStyles:[
        {
          when: row => row.ranking % 2 === 0, 
          style: {
            backgroundColor: "#D3D3D3"           
            // opacity: 20%,
          }
        }
      ]
    }, 

    {
      name: "Stock Name", 
      selector: row => row.name,
      conditionalCellStyles:[
        {
          when: row => row.ranking % 2 === 0, 
          style: {
            backgroundColor: "#D3D3D3"           
            // opacity: 20%,
          }
        }
      ]
    }, 

    {
      name: "Beat Index",
      selector: row => row.index,
      conditionalCellStyles:[
        {
          when: row => row.ranking % 2 === 0, 
          style: {
            backgroundColor: "#D3D3D3"           
            // opacity: 20%,
          }
        }
      ]
    },

    {
      name: "Current Price ($)", 
      selector: row => row.price,
      conditionalCellStyles:[
        {
          when: row => row.ranking % 2 === 0, 
          style: {
            backgroundColor: "#D3D3D3"           
            // opacity: 20%,
          }
        }
      ]
    }
  ]

  const info = [
    {"ranking": 1, "name": "ABC", "index": 0, "price":0}, 
    {"ranking": 2,"name": "ABC", "index": 0, "price":0}, 
    {"ranking": 3,"name": "ABC", "index": 0, "price":0}]

  return (

    // I used DataTable component from react-data-table-component module https://www.youtube.com/watch?v=lZDnUubIUOg&ab_channel=M%C3%BChendisBa%C4%9Fyan

    <DataTable columns={columns} data={info} fixedHeader expandableRows/>


  )

}


export default CustomTable;