import React, { createContext, useReducer } from "react";
import AppReducer from './AppReducer.js';

//tweets will be mapped to this dataset

const initialState = {
    loading:false,
    title:"nill",
    searchModels: "", 
    rankingModel: [],
    tweets: [
        {
            id: 1,
            user: {
                name: 'The White House',
                image: 'https://pbs.twimg.com/profile_images/1059888693945630720/yex0Gcbi_bigger.jpg',
                handle: '@WhiteHouse',
            },
            tweet: {
                content: 'On World Health Day, 2020, "we reaffirm our commitment to do our part to stop the spread of this virus, care for the sick, and protect the health and well-being of our fellow Americans."',
                image: 'https://pbs.twimg.com/card_img/1246823270524973058/IbkZhS3u?format=jpg&name=small',
                comments: '100',
                retweets: '320',
                likes: '1k',
                relevance: "nil"
            }
        },
        {
            id: 2,
            user: {
                name: 'Barack Obama',
                image: 'https://pbs.twimg.com/profile_images/822547732376207360/5g0FC8XX_bigger.jpg',
                handle: '@BarackObama',
            },
            tweet: {
                content: `My advisor and friend @cecmunoz has been someone I’ve turned to for years. In her new book, More Than Ready, she shares her story and an empowering message to women, especially women of color, that they are the leaders we need to make a change in our world.`,
                image: 'https://pbs.twimg.com/media/EVBZFzbXkAA95FX?format=jpg&name=small',
                comments: '2k',
                retweets: '5k',
                likes: '10k',
                relevance: "nil"
            }
        },
    ]

}

// create context
export const GlobalContext = createContext(initialState);

// provider
export const GlobalProvider = ({ children }) => {
    const [state, dispatch] = useReducer(AppReducer, initialState);
    function setLoading(payload){
        dispatch({
            type: "SET_LOADING",
            payload:payload
        })
    }

    function addRankingScore(payload){
        payload.push(state.searchModels)
        dispatch({
            type: "ADD_RANKING_SCORE",
            payload:payload
        })
    }

    function setSearchModels(model){
        dispatch({
            type: "SET_SEARCH_MODEL",
            payload:model
        })
    }

    function getTweet(id) {
        return state.tweets.find(tweet => tweet.id == id);
    }

    function setTitle(title) {
        dispatch({
            type: "SET_TITLE",
            payload: title
        })
    }

    function addTweet(tweets) {
        dispatch({
            type: 'ADD_TWEET',
            payload: tweets
        })
    }

    function removeAllTweets(){
        dispatch({
            type:"REMOVE_ALL_TWEETS"
        })
    }

    return (
    <GlobalContext.Provider 
        value={{ tweets: state.tweets, 
                setTitle, 
                getTweet, 
                addTweet,
                rankingModel: state.rankingModel, 
                title:state.title, 
                setSearchModels,
                removeAllTweets,
                addRankingScore,
                searchModels:state.searchModels}}>
        {children}
    </GlobalContext.Provider>)
}
