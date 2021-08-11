import React, { useState, useEffect, useContext } from 'react';
import '../styles/Main.css';
import { TweetList } from '../components/TweetList';
import { SearchIcon } from '../images/svg/svgs'
import * as API from "../apifunctions"
import { Button } from '@material-ui/core';
import { GlobalContext } from '../context/GlobalState'
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';


export const Home = () => {
    const [titlesState, setTitlesState] = useState([])
    const { title, setTitle, loading } = useContext(GlobalContext);


    const classes = useStyles();
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

                const randomElement = values[Math.floor(Math.random() * titlesState.length)];
                setTitle(randomElement)
                setTitlesState(values)
            }
        ).catch(
            err => console.log("Error fetching titles", err)
        )
    }, [])

    const randomButtonClick = () => {
        if (titlesState.length == 0){
            return alert("Thee are no test article titles in the front end yet! You must first retrieves test article titles from the back end! the back end is likely still starting up or has yet to be connected\
            if you are sure the backend is connected, try refreshing the page \
            ")
        }
        const randomElement = titlesState[Math.floor(Math.random() * titlesState.length)];
        setTitle(randomElement)
    }
    return (
        <>
            <div style = {{display:"flex", flexDirection:"row", alignItems:"center"}}> 
            {/*
            <div className="search-box flex-align-center">
                    <SearchIcon />
                    <input placeholder="Search Our Corpus Using Headlines" className="search-input w-100" type="text" />
            </div>
            */}
            <Button
                onClick = {randomButtonClick}
                variant="contained" 
                style = {{height:"50%", marginRight:"15px"}}
                color="primary">
                Get Random Title
            </Button>

            <h2 style = {{display:"flex", alignItems:"center", textAlign:"center"}}>
                Current Search Title:
            </h2>
            
            </div>

            <Backdrop className={classes.backdrop} open={true} onClick={() => {}}>
                <div style = {{display:"flex", flexDirection:"column", alignItems:"center"}}>
            <h2>
                currently retrieving relevant tweets....
            </h2>
            <CircularProgress color="inherit" />
            </div>
            </Backdrop>
        

            <h2 style = {{display:"flex", justifyContent:"center"}}>

                {title.title}
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

const useStyles = makeStyles((theme) => ({
    backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
    },
}));

