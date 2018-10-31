import logging
from logging import Logger
from logging.config import fileConfig
from .riot import Riot
from .utils import write_json, get_participant_wins, getSomething
from .loldb import Loldb
from typing import Dict, List, Tuple
from math import inf


class LolCrawler:
    """
    order of operations:
        crawl() { start with seed player and keep going } ->
            crawl_player() { get matchlist for player } ->
                iterate_matchlist() { get each match } ->
                    handle_match() { abstract, you should handle participants and everything here }
    """

    def __init__(self, api_key: str, dbname="lolcrawler.db"):
        """
        __init__ is called when the object is created from the class
        here you can add variables to self so you can access them later from one of your methods
        methods are the functions below
        :param api_key:
        :param dbname:
        """
        fileConfig("logging.conf")
        self.logger: Logger = logging.getLogger()
        self.logger.debug("--- debugging ---")

        # a function to get a dictionary of wins from the match data
        self.get_participant_wins = get_participant_wins

        # get ready to call the API
        self.riot = Riot(api_key)

        self.player_wins = dict()
        self.db_name = dbname
        self.api_key = api_key

        # create the database
        self.db = Loldb(dbname)

    def handle_match(self, match_id: int) -> None:
        """
        this gets overridden by MatchCrawler
        where all of the getting and inserting logic is
        :param match_id:
        :return:
        """
        pass

    def iterate_matchlist(self, match_list: Dict) -> None:
        """
        goes over a list of matches
        and hands the match ids to handle_match
        which is in MatchCrawler
        :param match_list:
        :return:
        """
        match_list = match_list['matches']
        for m in match_list:
            try:
                match_id = m['gameId']

                # skip it if it's already been covered
                if self.db.matchlist_contains(match_id):
                    continue

                self.handle_match(match_id)
            except Exception as ex:
                self.logger.exception(ex)

    def crawl_player(self, seed_player_id: int) -> None:
        """
        given a player id it  gets their match list
        and hands off their matchlist
        :param seed_player_id:
        :return:
        """
        # if we've covered this player skip
        if self.db.in_matchlists(seed_player_id):
            return
        match_list = self.riot.getMatchList(seed_player_id)
        self.iterate_matchlist(match_list)
        # update table of matchlists
        cmd = "insert into matchlists values ({})".format(seed_player_id)
        self.db.execute(cmd)

    def crawl(self, seed_player_id: int, iterations: int=inf) -> None:
        """
        starts with one player and randomly selects players to get their matchlist
        continues to get match ids for infinity or a specified value
        :param seed_player_id:
        :param iterations:
        :return:
        """
        self.crawl_player(seed_player_id)
        counter = 0
        while counter < iterations:
            counter += 1

            new_player = self.db.get_random_participant()
            self.crawl_player(new_player)



if __name__ == "__main__":
    # don't do it here
    # use MatchCrawler
    riot_key = "RGAPI-8a656aec-4c0d-47dd-9c37-ce52288b6f14"
    seed_player = 50068799  # "Faker"
    db_name = "lolcrawler.db"

    lolcrawler = LolCrawler(api_key=riot_key, dbname=db_name)
    lolcrawler.crawl(seed_player)
