import React, {useContext} from 'react';
import { Trend } from '../trending/Trend';
import { SettingsIcon } from '../../images/svg/svgs';

import { GlobalContext } from '../../context/GlobalState'


export const TrendsList = () => {

    const {rankingModel} = useContext(GlobalContext);


    const trends = [
        {
            name: '#Modiji_Ban_TikTok',
            topic: '',
            tweets: '3,700k'
        }
    ]
    return (
        <div>
            <div className="trends-for-you flex-space-between">
                <h2 className="m-0">Score Table</h2>
                <h3 className="m-0">Non Discounted Cumulative Gain </h3>
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
