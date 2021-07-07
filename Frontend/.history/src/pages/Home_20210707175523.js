import React from 'react'
import { NewTweet } from '../components/NewTweet';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'



export const Home = () => {
    return (
        <>
    

            <div className="search-box flex-align-center">
                    <SearchIcon />
                    <input placeholder="Search Our Corpus" className="search-input w-100" type="text" />
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
