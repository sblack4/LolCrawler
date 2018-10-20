import sqlite3
import logging
from logging import Logger
from logging.config import fileConfig
from riot import Riot
from utils import write_json, get_participant_wins, getSomething
from loldb import Loldb
from time import sleep
from typing import Dict, List, Tuple


class LolCrawler:

    def __init__(self, api_key: str, dbname="lolcrawler.db"):
        fileConfig("logging.conf")
        self.logger: Logger = logging.getLogger("root")

        self.logger.debug("--- debugging ---")

        self.riot = Riot(api_key)

        self.player_wins = dict()

        self.db = Loldb(dbname)

    def insert_timeline(self, timeline: dict) -> None:
        elements = ['creepsPerMinDeltas', 'xpPerMinDeltas', 'goldPerMinDeltas', 'damageTakenPerMinDeltas']
        part_id = str(timeline['participantId'])
        did_win = str(self.player_wins[int(part_id)])
        command = "insert into timelines values (" + part_id + ", " + did_win
        for e in elements:
            x, y = getSomething(timeline, e)
            command = command + ", " + str(x) + ", " + str(y)
        command += ")"
        self.db.execute(command)

    def iterate_players(self, player_list):
        for p in player_list:
            timeline = p['timeline']
            self.insert_timeline(timeline)
        self.db.commit()

    def handle_match(self, match_id: int) -> None:
        match = self.riot.getMatch(match_id)

        self.player_wins = get_participant_wins(match)
        participantIdentities = match['participantIdentities']
        self.db.insert_participants(participantIdentities)

        players = match['participants']
        self.iterate_players(players)
        self.db.execute("insert into matches values ('{}')".format(match_id))

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

    def crawl(self, seed_player_id: int) -> None:
        if self.db.in_matchlists(seed_player_id):
            return
        match_list = self.riot.getMatchList(seed_player_id)
        write_json(match_list, str(seed_player_id) + "-match-list.json")
        self.iterate_matchlist(match_list)
        # update table of matchlists
        cmd = "insert into matchlists values ({})".format(seed_player_id)
        self.db.execute(cmd)



if __name__ == "__main__":
    riot_key = "RGAPI-eb49c30b-3d29-4160-a19a-3ab744f48aa0"
    seed_player = 50068799  # "Faker"
    db_name = "lolcrawler.db"

    lolcrawler = LolCrawler(riot_key)
    lolcrawler.crawl(seed_player)
    while True:
        conn = sqlite3.connect(db_name)
        curr = conn.cursor()
        command = "select accountId from participants ORDER BY RANDOM() LIMIT 1"
        curr.execute(command)
        new_player = curr.fetchone()[0]
        curr.close()
        conn.close()

        lolcrawler = LolCrawler(riot_key)
        lolcrawler.crawl(new_player)
