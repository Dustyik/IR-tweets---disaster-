import axios from 'axios';

const getData = async () => {
    await axios.get("http://localhost:5000/getTitles")
    .then((res) => {
        console.log(res)
    })
}