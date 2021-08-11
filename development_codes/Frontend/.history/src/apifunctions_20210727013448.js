import axios from 'axios';

export const getTitles = () => {
    console.log("get Titles called")
    return axios.get("http://localhost:5000/getTitles")
}   

export const applySearchFilters = (data) => {
    return axios.post("http://localhost:5000/applySearchModels",
    {data: data}
    )
}
