export default (state, action) => {
    switch (action.type) {
        case 'DELETE_TRANSACTION':
            return {
                ...state,
                transactions: state.transactions.filter(transaction => transaction.id !== action.payload)
            }
        case 'ADD_TWEET':
            const newTweet = {
                user: {
                    name: 'Bharath',
                    image: 'https://pbs.twimg.com/profile_images/1247964769669136385/KVCROk2D_bigger.jpg',
                    handle: '@bharathravi27',
                },
                tweet: {
                    content: action.payload,
                    image: null,
                    time: '10m',
                    comments: '100',
                    retweets: '320',
                    likes: '1k'
                }
            };
            return {
                ...state,
                tweets: [...state.tweets, newTweet]
            }

        case "SET_TITLE":
            return {
            ...state,
            title: action.payload
        }

        case "ADD_SEARCH_MODEL":
            console.log(typeof(state.searchModels))
            console.log(state.searchModels)
            const newSearchModels = state.searchModels.push(action.payload)
            console.log(newSearchModels)
            return {
            ...state,
            searchModels: newSearchModels
        }
        default:
            return state
    }
}