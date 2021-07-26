import axios from 'axios';

export const getTitles = async () => {
    return axios.get("http://localhost:5000/getTitles")
}   
