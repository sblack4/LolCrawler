#!/bin/bash



echo "enter api key"
#read api_key
api_key="RGAPI-aa4df822-5310-4608-a56f-8d8a955b3729"

base_route="https://na1.api.riotgames.com"

api_arg="?api_key=$api_key"

match_id=2842707542

[ ! -e data ] && mkdir data

echo "getting match 2842707542"
get_match="https://na1.api.riotgames.com/lol/match/v3/matches/"
curl "$get_match$match_id?api_key=$api_key" \
    -o data/example_match.json


echo "getting timeline for match"
get_timeline="/lol/match/v3/timelines/by-match/"
curl_arg="$base_route$get_timeline$match_id$api_arg"
echo $curl_arg
#curl  $curl_arg \
#    -o data/example_timeline.json
