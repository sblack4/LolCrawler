import sqlite3
from sqlite3 import IntegrityError
import logging
from typing import Dict, Union


class Loldb(object):
    def __init__(self, dbname="lolcrawler.db"):
        self.logger = logging.getLogger("lolcrawler")

        self.conn = sqlite3.connect(dbname)
        self.curr = self.conn.cursor()
        self.after_init_hook()

    def after_init_hook(self):
        pass

    def create_participantdb(self):
        self.create_participant_table()
        self.create_timeline_table()
        self.create_matches_table()
        self.create_matchlist_table()

    def close(self) -> None:
        self.curr.close()
        self.conn.close()

    def commit(self) -> None:
        self.conn.commit()

    def execute(self, command: str) -> None:
        self.curr.execute(command)

    def check_table_exists(self, table_name: str) -> bool:
        command = "select count(*) from sqlite_master " \
            "WHERE name='{}'".format(table_name)
        self.curr.execute(command)
        if self.curr.fetchone()[0] == 1:
            return True
        return False

    def create_participant_table(self) -> None:
        if self.check_table_exists('participants'):
            return
        command = (""
                   "        CREATE TABLE `participants` ("
                   "        	`pname`	text,"
                   "        	`platform`	text,"
                   "        	`accountId`	int UNIQUE,"
                   "        	`summonerId`	int"
                   "        );"
                   "        ")
        self.curr.execute(command)
        self.conn.commit()

    def create_timeline_table(self) -> None:
        """
        creates timeline table if it does not exist
        """
        if self.check_table_exists('timelines'):
            return
        command = "create table timelines " + \
                  "(participantId, win, creepD1, creepD2, xpD1, xpD2, goldD1, goldD2, damageD1, damageD2)"
        self.curr.execute(command)
        self.conn.commit()

    def create_matches_table(self) -> None:
        if self.check_table_exists("matches"):
            return
        command = "create table matches (gameId, unique(gameId))"
        self.curr.execute(command)
        self.conn.commit()

    def create_matchlist_table(self) -> None:
        if self.check_table_exists("matchlists"):
            return
        command = "CREATE TABLE matchlists (accountId, unique(accountId))"
        self.curr.execute(command)
        self.conn.commit()

    def matchlist_contains(self, match_id: Union[str, int]) -> bool:
        command = "select count(*) from matches where gameId = '{}'".format(match_id)
        self.curr.execute(command)
        result = self.curr.fetchone()[0]
        if result > 0:
            return True
        return False

    def insert_participants(self, participants_list: Dict) -> None:
        for p in participants_list:
            try:
                p = p['player']
                pname = p['summonerName']
                platformId = p['platformId']
                accountId = p['accountId']
                summonerId = p['summonerId']
                command = """
                insert into participants values
                ('{pname}', '{platformId}', {accountId}, {summonerId})
                """.format(pname=pname, platformId=platformId, accountId=accountId, summonerId=summonerId)
                self.curr.execute(command)

            except IntegrityError as ex:
                self.logger.warning(ex)
            except Exception as ex:
                self.logger.warning(ex)

        self.conn.commit()

    def get_random_participant(self) -> int:
        command = "select accountId from participants ORDER BY RANDOM() LIMIT 1"
        self.db.curr.execute(command)
        new_player = self.db.curr.fetchone()[0]
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
