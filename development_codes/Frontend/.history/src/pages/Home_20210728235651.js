import React, { useState, useEffect, useContext } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"
import Button from 'react-bootstrap/Button'
import { GlobalContext } from '../context/GlobalState'


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])
    const { title, setTitle } = useContext(GlobalContext);


    useEffect(() => {
        console.log("Getting Titles")
        API.getTitles().then(
            res => {
                const data = JSON.parse(res.data);
                const titlesData = data.title
                console.log(titlesData)
                const idData = data.id
                values = []
                var values = Object.keys(titlesData).map(
                    function(key){
                    return {
                        title:titlesData[key]
                });
                setTitlesState(values)
            }
        ).catch(
            err => console.log("Error fetching titles", err)
        )
    }, [])

    const randomButtonClick = () => {
        const randomElement = titlesState[Math.floor(Math.random() * titlesState.length)];
        setTitle(randomElement)
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
            <h2 style = {{display:"flex", justifyContent:"center"}}>
                Current Search Title:
            </h2>

            <h2 style = {{display:"flex", justifyContent:"center"}}>
               {title}
            </h2>
                {/*
            <NewTweet />
                */}
            <div className="tweets">
                <TweetList />
            </div>
        </>
    )
}
