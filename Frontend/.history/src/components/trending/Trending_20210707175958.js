import React from 'react';
import '../../styles/Trending.css';
import { SearchIcon } from '../../images/svg/svgs'
import { TrendsList } from './TrendsList';
import { FollowSuggestionsList } from './FollowSuggestionsList';


export const Trending = () => {
    return (
        <>
            <div>

                <div className="trends-list m-0">
                    {/*
                    <TrendsList />
                    */}
                    <h3>
                    Corresponding Precision and Recall Scores
                    </h3>
                </div>
                {/*
                <div className="follow-list">
                    <FollowSuggestionsList />
                </div>
                */}
            </div>
        </>
    )
}
