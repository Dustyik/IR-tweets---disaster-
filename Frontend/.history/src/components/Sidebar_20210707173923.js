import React from 'react';
import { Logo, HomeIcon, ExploreIcon, NotificationIcon, MessageIcon, BookmarkIcon, ListsIcon, MoreIcon } from '../images/svg/svgs';
import { SmallAvatar } from '../images/avatars';
import { Checkbox } from '@material-ui/core';

export const Sidebar = () => {
    const profImageurl = 'https://pbs.twimg.com/profile_images/1247964769669136385/KVCROk2D_bigger.jpg';
    return (
        <div>
            <div className="side-nav-header">
                <Logo />
            </div>
            <div>
                different search models
            </div>

            <div>
            <Checkbox
            size = "medium"
            >
            </Checkbox>
                different search models
            </div>
          
          

        

        </div>
    )
}
