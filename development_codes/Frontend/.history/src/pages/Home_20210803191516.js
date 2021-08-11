import React, { useState, useEffect, useContext } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"
import { Button } from '@material-ui/core';
import { GlobalContext } from '../context/GlobalState'


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])
    const { title, setTitle } = useContext(GlobalContext);


    useEffect(() => {
        API.getTitles().then(
            res => {
                const data = JSON.parse(res.data);
                const titlesData = data.title
                const idData = data.id
                var values = []
                for (let i = 0; i < Object.keys(titlesData).length; i++){
                    values.push({
                        title: titlesData[i],
                        id: idData[i]
                    })
                }
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
        <div style = {{display:"flex", flexDirection:"row"}}> 
                <div
                style = {{display:"flex", justifyContent:"center",}}
                >
               
                <Button
                    onClick = {randomButtonClick}
                    variant="contained" 
                    color="primary">
                    Get Random Title
                </Button>
                </div>
               
                <h2 style = {{display:"flex", justifyContent:"center"}}>
                    Current Search Title:
                </h2>

                <h2 style = {{display:"flex", justifyContent:"center"}}>
                {title.title}
                </h2>
             
            <div className="tweets">
                <TweetList />
            </div>
        </div>
  
    )
}
