"""
get timeline summary data from the participants list
insert it into a sqllite database
"""
import logging
from logging import Logger
from logging.config import fileConfig
from riot import Riot
from utils import get_participant_wins, getSomething
from loldb import Loldb
from typing import Dict
from math import inf
from lolcrawler import lolcrawler


logger = logging.getLogger(__name__)


class MatchCrawler(lolcrawler):
    def after_init_hook(self):
        # tables are already created
        print("tables are created, TODO: create create table sql")
        pass

    def handle_match(self, match_id: int) -> None:
        match = self.riot.getMatch(match_id)



if __name__ == "__main__":
    riot_key = "RGAPI-48aed195-b319-4954-86ad-a58352ce2c01"
    seed_player = 50068799  # "Faker"
    db_name = "lolcrawler.db"

    matchcrawler = MatchCrawler(api_key=riot_key, dbname=db_name)
    matchcrawler.crawl(seed_player)
