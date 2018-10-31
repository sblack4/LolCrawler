# lolcrawler
Get data from the Riot API and put it into a SQLLite database

1. `Lolcrawler` takes a player identity and gets their match list
1. it takes each match id and, if we haven't done it yet, hands it to `handle_match()`
1. `MatchCraler` has `handle_match()` and get the match data from the riot API
1. then it inserts all of the data (that I've set it up to so far) into the database
1. then `Lolcrawler` gets a random player from the player's table and repeats

## Idea 
We have a SQLLite Database and this app to 
1. get a random player from the database we haven't done yet
1. get all their matches we haven't covered yet
1. get all the information for that match & insert into database
1. get all the timeline data for that match & insert into database
1. mark that player covered and start again from one

The default seed player is set to [Faker](https://lol.gamepedia.com/Faker)