import axios from 'axios';

export const getTitles = () => {
    console.log("get Titles called")
    return axios.get("http://localhost:5000/getTitles").then(
        res => res
    )
}   

export const applySearchFilters = () => {
    return axios.post("http://localhost:5000/applySearchModels").then(
        res => res
    )
}
