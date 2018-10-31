#!/bin/bash



echo "enter api key"
#read api_key
api_key="RGAPI-8dc9be1b-5b2a-4db5-8cb6-66ec939033e8"

base_route="https://na1.api.riotgames.com"

api_arg="?api_key=$api_key"

match_id=2842707542

[ ! -e data ] && mkdir data

get_match(){
    echo "getting match 2842707542"
    get_match="https://na1.api.riotgames.com/lol/match/v3/matches/"
    curl "$get_match$match_id?api_key=$api_key" \
        -o data/example_match.json
}

get_timeline(){
    echo "getting timeline for match"
    get_timeline="/lol/match/v3/timelines/by-match/"
    curl_arg="$base_route$get_timeline$match_id$api_arg"
    echo ${curl_arg}
    curl  ${curl_arg} \
        -o data/example_timeline.json
}

get_summoner_by_name(){
    player_name="Faker"
    get_summoner="/lol/summoner/v3/summoners/by-name/"
    curl_arg="$base_route$get_summoner$player_name$api_arg"
    echo ${curl_arg}
    curl ${curl_arg} \
        -o data/example-summoner-by-name.json
}

get_summoner_by_id(){
    player_name=50068799
    get_summoner="/lol/summoner/v3/summoners/by-account/"
    curl_arg="$base_route$get_summoner$player_name$api_arg"
    echo ${curl_arg}
    curl ${curl_arg} \
        -o data/example-summoner-by-id.json
}


get_summoner_by_name

get_summoner_by_id
