import React from 'react';
import { Logo, HomeIcon, ExploreIcon, NotificationIcon, MessageIcon, BookmarkIcon, ListsIcon, MoreIcon } from '../images/svg/svgs';
import { SmallAvatar } from '../images/avatars';
import { Checkbox } from '@material-ui/core';
import { Button } from '@material-ui/core';

export const Sidebar = () => {
    const profImageurl = 'https://pbs.twimg.com/profile_images/1247964769669136385/KVCROk2D_bigger.jpg';
    return (
        <div>
            <div className="side-nav-header">
                <Logo />
            </div>
            <div>
                <text>
                Different Search Models 
                {"\n"}

                Different Combinations can be used to get different search results
                </text>
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                Search Model 1
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                Search Model 2
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                Search Model 3
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                Search Model 4
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                Search Model 5
            </div>
          
            <Button variant="contained" color="primary">
                Apply Filter
            </Button>

        

        </div>
    )
}
