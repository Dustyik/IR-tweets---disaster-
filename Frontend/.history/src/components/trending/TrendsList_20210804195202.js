import React, {useContext} from 'react';
import { Trend } from '../trending/Trend';
import { SettingsIcon } from '../../images/svg/svgs';

import { GlobalContext } from '../../context/GlobalState'


export const TrendsList = () => {

    const {rankingModel} = useContext(GlobalContext);


    const trends = [
        {
            name: '#Modiji_Ban_TikTok',
            topic: 'Trending in India',
            tweets: '3,700k'
        }
    ]
    return (
        <div>
            <div className="trends-for-you flex-space-between">
                <h1 className="m-0">Trends for you</h1>
                <SettingsIcon />
            </div>
            <div>
                {rankingModel}
                {console.log("scores", rankingModel)}
            </div>
            <div className="trends">
                {trends.map(trend => (<Trend trend={trend} />))}
            </div>
        </div>
    )
}
