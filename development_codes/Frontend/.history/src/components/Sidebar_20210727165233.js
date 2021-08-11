import React, {useState, useContext} from 'react';
import { Logo, HomeIcon, ExploreIcon, NotificationIcon, MessageIcon, BookmarkIcon, ListsIcon, MoreIcon } from '../images/svg/svgs';
import { SmallAvatar } from '../images/avatars';
import { Checkbox } from '@material-ui/core';
import { Button } from '@material-ui/core';
import * as API from "../apifunctions"
import { GlobalContext } from '../context/GlobalState'

const SEARCH_MODELS = ["Tf-idf w Cosine Sim", "Tf-idf w Euclidean Dist"]

export const Sidebar = () => {
    const profImageurl = 'https://pbs.twimg.com/profile_images/1247964769669136385/KVCROk2D_bigger.jpg';
    const [searchModelsLocalState, setSearchModelsLocalState] = useState([])

    const {setSearchModels, searchModels, title} = useContext(GlobalContext);

    const checkBoxToggled = (event) => {
        const id = event.id
        const checkValue = event.checked

        if (checkValue){
            setSearchModels(id)
            setSearchModelsLocalState(id)
        }
    }

    const applyFilter = () => {
        API.applySearchFilters(searchModels, title).then(
            res => console.log(res)
        )
    }

    const createCheckBoxes = () => 
        SEARCH_MODELS.map((e) => {

            return (
                <div>
                <Checkbox
                size = "medium"
                id = {e}
                onChange = {(e) => checkBoxToggled(e.target)}
                checked = {searchModelsLocalState == e}
                >
                </Checkbox>
                {e}
                </div>
            )
        }
    )
            

    const checkBoxes = createCheckBoxes()

    return (
        <div>
            <div className="side-nav-header">
                
                <h1>
                <Logo />
                    NewsTweet
                </h1>
            </div>
            <h4>
                Different Search Models, 
                Choose 1
            </h4>

 

            {checkBoxes}
            
            <Button 
                onClick = {applyFilter}
                variant="contained" color="primary">
                Apply Filter
            </Button>

        

        </div>
    )
}
