"""
get timeline summary data from the participants list
insert it into a sqllite database
"""
import logging
from logging import Logger
from logging.config import fileConfig
from lolcrawler.riot import Riot
from utils import get_participant_wins, getSomething
from loldb import Loldb
from typing import Dict
from math import inf
from lolcrawler.lolcrawler import lolcrawler
from lolcrawler.loldb import Loldb


logger = logging.getLogger(__name__)


class EventDb(Loldb):
    """ tables:
    - participants
    - matches   (matches
    - matchlists (accounts we already have matches for)
    - events    (events)
    - timelines (participant frames)
    """

    def after_init_hook(self):
        self.create_participant_table()
        self.create_timeline_table()
        self.create_matches_table()
        self.create_matchlist_table()





if __name__ == "__main__":
    riot_key = "RGAPI-aa4df822-5310-4608-a56f-8d8a955b3729"
    seed_player = 50068799  # "Faker"
    db_name = "lolcrawler.db"

    lolcrawler = LolCrawler(api_key=riot_key, dbname=db_name)
    lolcrawler.crawl(seed_player)
