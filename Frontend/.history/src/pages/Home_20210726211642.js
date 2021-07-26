import React from 'react'
import { NewTweet } from '../components/NewTweet';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import axios from 'axios';


export const Home = () => {

    const getData = async () => {
        await axios.get("http://localhost:5000/getTitles", "getting titles...")
        .then((res) => {
            console.log(res)
        })
    }

    return (
        <>
    
    <button onClick={getData} >CONNECT</button>

            <div className="search-box flex-align-center">
                    <SearchIcon />
                    <input placeholder="Search Our Corpus Using Headlines" className="search-input w-100" type="text" />
                </div>
                {/*
            <NewTweet />
                */}
            <div className="tweets">
                <TweetList />
            </div>
        </>
    )
}
