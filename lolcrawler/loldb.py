"""
facade over the database
and has some logic to do database stuff
"""
import sqlite3
from logging import Logger
from sqlite3 import IntegrityError
import logging
from logging.config import fileConfig
from typing import Dict, Union


class Loldb(object):
    def __init__(self, dbname="lolcrawler.db"):
        fileConfig("logging.conf")
        self.logger: Logger = logging.getLogger()

        self.conn = sqlite3.connect(dbname)
        self.curr = self.conn.cursor()

    def close(self) -> None:
        self.logger.info("--- closing db curr and conn ---")
        self.curr.close()
        self.conn.close()

    def commit(self) -> None:
        self.logger.info("--- Commiting ---")
        self.conn.commit()

    def execute(self, command: str) -> None:
        self.logger.info("--- executing command: \n {} \n".format(command))
        self.curr.execute(command)

    def check_table_exists(self, table_name: str) -> bool:
        command = "select count(*) from sqlite_master " \
            "WHERE name='{}'".format(table_name)
        self.curr.execute(command)
        if self.curr.fetchone()[0] == 1:
            return True
        return False

    def matchlist_contains(self, match_id: Union[str, int]) -> bool:
        command = "select count(*) from MatchDto where gameId = '{}'".format(match_id)
        self.curr.execute(command)
        result = self.curr.fetchone()[0]
        if result > 0:
            return True
        return False

    def get_random_participant(self) -> int:
        command = "select accountId from PlayerDto ORDER BY RANDOM() LIMIT 1"
        self.curr.execute(command)
        new_player = self.curr.fetchone()[0]
        return new_player

    def in_matchlists(self, accountId: int) -> bool:
        command = "select count(*) from matchlists where accountId = {}".format(int(accountId))
        self.curr.execute(command)
        result = self.curr.fetchone()[0]
        if result > 0:
            return True
        return False



if __name__ == "__main__":
    pass
