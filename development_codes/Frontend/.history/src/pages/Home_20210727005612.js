import React, { useState, useEffect } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"
import Button from 'react-bootstrap/Button'


export const Home = () => {
    const [currentSearchTitle, setCurrentSearchTitle] = useState("nil")
    const [titlesState, setTitlesState] = useState([])

    useEffect(() => {
        console.log("Getting Titles")
        API.getTitles().then(
            res => {
                console.log("Response from server")
                var dictionary = JSON.parse(res.data);
            
                var values = Object.keys(dictionary).map(
                    function(key){
                    return dictionary[key];
                });
                setTitlesState(values)
            }
        ).catch(
            err => console.log("Error fetching titles", err)
        )
    }, [])

    const randomButtonClick = () => {
        const randomElement = titlesState[Math.floor(Math.random() * titlesState.length)];
        alert(titlesState)
    }
    
    return (
        <>
        <div style = {{display:"flex", flexDirection:"row"}}> 
            <div className="search-box flex-align-center">
                    <SearchIcon />
                    <input placeholder="Search Our Corpus Using Headlines" className="search-input w-100" type="text" />
            </div>
            <Button
                className="btn-primary"
                variant="outline-primary"
                size = "lg"

                onClick = {randomButtonClick}
            >
                Random Search Button
            </Button>
            </div>

            <h3 style = {{alignItems:"center"}}>
                {currentSearchTitle}
            </h3>
                {/*
            <NewTweet />
                */}
            <div className="tweets">
                <TweetList />
            </div>
        </>
    )
}
