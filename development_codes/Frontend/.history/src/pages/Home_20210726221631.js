import React, { useState, useEffect } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])

    useEffect(() => {
        const titles = API.getTitles()
        console.log(titles)
    })
    
    return (
        <>


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
