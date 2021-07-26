import React, { useState, useEffect } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"
import Button from 'react-bootstrap/Button'


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])

    useEffect(() => {
        console.log("Getting Titles")
        API.getTitles().then(
            res => {
                console.log("Response from server")
                console.log(typeof(res.data))
                var dictionary = JSON.parse(res.data);
            
                var values = Object.keys(dictionary).map(
                    function(key){
                    return dictionary[key];
                });
                //setTitlesState(values)
            }
        ).catch(
            err => console.log("Error fetching titles", err)
        )
    }, [titlesState])
    
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
            >
                Random Search Button
            </Button>
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
