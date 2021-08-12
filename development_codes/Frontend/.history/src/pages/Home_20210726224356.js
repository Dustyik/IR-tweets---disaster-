import React, { useState, useEffect } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])

    useEffect(() => {
        API.getTitles().then(
            res => console.log(res)
        )
    })
    
    return (
        <>
        <div style = {{display:"flex", flexDirection:"row"}}> 
            <div className="search-box flex-align-center">
                    <SearchIcon />
                    <input placeholder="Search Our Corpus Using Headlines" className="search-input w-100" type="text" />
            </div>
            <div style = {{alignItems:"center"}}>
                test
            </div>
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