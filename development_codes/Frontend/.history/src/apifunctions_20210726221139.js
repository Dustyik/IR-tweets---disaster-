import axios from 'axios';

const getTitles = async () => {
    return await axios.get("http://localhost:5000/getTitles")
    .then((res) => {
        console.log(res)
    })
}
module.exports = {
    getTitles: getTitles,
}