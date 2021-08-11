import axios from 'axios';

const getData = async () => {
    return await axios.get("http://localhost:5000/getTitles")
    .then((res) => {
        console.log(res)
    })
}
module.exports = {
    getTitles: getData,
}