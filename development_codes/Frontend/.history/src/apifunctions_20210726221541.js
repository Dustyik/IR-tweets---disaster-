import axios from 'axios';

export const getTitles = async () => {
    return await axios.get("http://localhost:5000/getTitles")
    .then((res) => res)
    .catch(err => console.log("Error fetching titles", err))
}   
