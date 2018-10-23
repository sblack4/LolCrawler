import sqlite3
import logging
from logging import Logger
from logging.config import fileConfig
from riot import Riot
from utils import write_json, get_participant_wins, getSomething
from loldb import Loldb
from lolcrawler import LolCrawler
from time import sleep
from typing import Dict, List, Tuple
from math import inf
import pandas as pd
from pandas import DataFrame


class TestLeagueDb(Loldb):

    def after_init_hook(self) -> None:
        self.create_participant_table()
        self.create_table_timestamp_long()
        self.create_matches_table()
        self.create_matchlist_table()

    def timestamp_long_columns(self) -> List[str]:
        columns = ['match_id']
        for frame_ind in range(60):
            columns.append("timestamp" + str(frame_ind))
            for participant_id in range(1, 11):
                columns.append("p" + str(participant_id) + 'x' + str(frame_ind))
                columns.append("p" + str(participant_id) + 'y' + str(frame_ind))
                columns.append("P" + str(participant_id) + "TotalGold" + str(frame_ind))
        columns.append("Winner")
        return columns

    def create_table_timestamp_long(self) -> None:
        table_name = "timelines_long"
        if self.check_table_exists(table_name):
            return
        columns = self.timestamp_long_columns()
        create_statement = "CREATE TABLE " + table_name + " (" + ", ".join(columns) + ")"
        self.curr.execute(create_statement)


class TestLeagueCrawler(LolCrawler):

    def after_init_hook(self):
        self.db = TestLeagueDb(self.db_name)

    def get_team_winnings(self, teams: List[Dict]) -> str:
        wins_dict = {x["teamId"]: x["win"] for x in teams}
        return [x for x, v in wins_dict.items() if v != "Fail"][0]

    def timeline_to_df(self, timeline: Dict, game_results: str, match_id: int) -> DataFrame:
        columns = self.db.timestamp_long_columns()
        df = {"match_id": match_id}  # pd.DataFrame(columns=columns)
        match_frames = timeline['frames']

        for frame_ind in range(len(match_frames)):

            time_step = "timestamp" + str(frame_ind)
            df[time_step] = (
                match_frames[frame_ind]["timestamp"]
            )

            # looping through the insane number of columns for each frame
            for participant_id in range(1, 11):
                x = "p" + str(participant_id) + 'x' + str(frame_ind)
                y = "p" + str(participant_id) + 'y' + str(frame_ind)
                p = "P" + str(participant_id) + "TotalGold" + str(frame_ind)
                try:
                    df[x] = (
                        match_frames[frame_ind]["participantFrames"][str(participant_id)]["position"]["x"]
                    )
                except KeyError as ke:
                    self.logger.debug(ke)
                    pass

                try:
                    df[y] = (
                        match_frames[frame_ind]["participantFrames"][str(participant_id)]["position"]["y"]
                    )
                except KeyError as ke:
                    self.logger.debug(ke)
                    pass

                try:
                    df[p] = (
                        match_frames[frame_ind]["participantFrames"][str(participant_id)]["totalGold"]
                    )
                except KeyError as ke:
                    self.logger.debug(ke)
                    pass

        df["Winner"] = game_results
        d_frame = pd.DataFrame(df, columns=columns, index=[0])
        return d_frame

    def handle_match(self, match_id: int) -> None:
        match = self.riot.getMatch(match_id)
        self.handle_participants(match)

        game_results = self.get_team_winnings(match["teams"])

        timeline = self.riot.getTimeline(match_id)
        df = self.timeline_to_df(timeline, game_results, match_id)
        df.to_sql(
            name="timelines_long",
            con=self.db.conn,
            if_exists="append",
            index=False
        )
        self.db.execute("insert into matches values ('{}')".format(match_id))



if __name__ == "__main__":
    riot_key = "RGAPI-a7c207e9-ce51-4bcf-bfe0-9c93406318e1"
    seed_player = 50068799  # "Faker"
    db_name = "test_league.db"

    testleaguecrawler = TestLeagueCrawler(
        api_key=riot_key,
        dbname=db_name
    )
    testleaguecrawler.crawl(seed_player)
