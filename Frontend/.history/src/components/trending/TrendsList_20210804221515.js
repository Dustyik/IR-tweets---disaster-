import React, {useContext} from 'react';
import { Trend } from '../trending/Trend';
import { SettingsIcon } from '../../images/svg/svgs';

import { GlobalContext } from '../../context/GlobalState'


export const TrendsList = () => {

    const {rankingModel} = useContext(GlobalContext);

    const trends = rankingModel.map((trend) => {
        return {
            name: trend[2],
            topic: '',
            tweets: trend[1]
        }

    }).reverse()
    return (
        <div>
            <div className="trends-for-you flex-space-between">
                <h2 className="m-0">Score Table</h2>
                <SettingsIcon />
            </div>
            <h3 style = {{padding:10}}className="m-0">Normalized Discounted Cumulative Gain </h3>

            <div>
            </div>
            <div className="trends">
                {trends.map(trend => (<Trend trend={trend} />))}
            </div>
        </div>
    )
}
