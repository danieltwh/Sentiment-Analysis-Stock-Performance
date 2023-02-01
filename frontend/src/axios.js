import axios from 'axios'

const instance = axios.create({
    baseURL: "https://nlp-stock-performance-backend.herokuapp.com"
})

export default instance