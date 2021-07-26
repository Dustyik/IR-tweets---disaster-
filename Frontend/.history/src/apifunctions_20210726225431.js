import axios from 'axios';

export const getTitles = () => {
    return axios.get("http://localhost:5000/getTitles")
}   
