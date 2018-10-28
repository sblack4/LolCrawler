import sqlite3
import logging
from logging import Logger
from logging.config import fileConfig
from riot import Riot
from utils import write_json, get_participant_wins, getSomething
from loldb import Loldb
from time import sleep
from typing import Dict, List, Tuple
from math import inf


class LolCrawler:
    """
    order of operations:
        crawl() ->
            crawl_player() { get matchlist for player } ->
                iterate_matchlist() { get each match } ->
                    handle_match() { abstract, you should handle participants and everything here }
    """

    def __init__(self, api_key: str, dbname="lolcrawler.db"):
        fileConfig("logging.conf")
        self.logger: Logger = logging.getLogger("root")
        self.logger.debug("--- debugging ---")

        self.get_participant_wins = get_participant_wins
        self.riot = Riot(api_key)

        self.player_wins = dict()
        self.db_name = dbname
        self.api_key = api_key

        self.db = Loldb(dbname)
        self.after_init_hook()

    def after_init_hook(self):
        pass

    def handle_match(self, match_id: int) -> None:
        pass

    def handle_participants(self, match: Dict) -> None:
        """gets player wins and insert identities into participants table"""
        self.player_wins = self.get_participant_wins(match)
        participantIdentities = match['participantIdentities']
        self.db.insert_participants(participantIdentities)

    def iterate_matchlist(self, match_list: Dict) -> None:
        match_list = match_list['matches']
        for m in match_list:
            try:
                match_id = m['gameId']

                # skip it if it's already been covered
                if self.db.matchlist_contains(match_id):
                    continue

                self.handle_match(match_id)
            except Exception as ex:
                self.logger.warning(ex)

    def crawl_player(self, seed_player_id: int) -> None:
        if self.db.in_matchlists(seed_player_id):
            return
        match_list = self.riot.getMatchList(seed_player_id)
        self.iterate_matchlist(match_list)
        # update table of matchlists
        cmd = "insert into matchlists values ({})".format(seed_player_id)
        self.db.execute(cmd)

    def crawl(self, seed_player_id: int, iterations: int=inf) -> None:
        self.crawl_player(seed_player_id)
        counter = 0
        while counter < iterations:
            counter += 1

            new_player = self.db.get_random_participant()
            self.crawl_player(new_player)



if __name__ == "__main__":
    riot_key = "RGAPI-aa4df822-5310-4608-a56f-8d8a955b3729"
    seed_player = 50068799  # "Faker"
    db_name = "lolcrawler.db"

    lolcrawler = LolCrawler(api_key=riot_key, dbname=db_name)
    lolcrawler.crawl(seed_player)
