"""
get timeline summary data from the participants list
insert it into a sqllite database
"""
from typing import List, Dict
from lolcrawler.lolcrawler import LolCrawler


class MatchCrawler(LolCrawler):
    """  """
    def after_init_hook(self):
        # tables are already created
        print("tables are created, TODO: create create table sql")
        pass

    def insert_match_data(self, match: object) -> bool:
        cols = ["seasonId",
                "queueId",
                "gameId",
                "gameVersion",
                "platformId",
                "gameMode",
                "mapId",
                "gameType",
                "gameDuration",
                "gameCreation"]
        start_cmd = "INSERT INTO MatchDto Values ("
        data: List[str] = []
        for col in cols:
            try:
                datum = "'" + str(match[col]) + "'"
            except:
                datum = "'null'"
            data.append(datum)
        cmd = start_cmd + ", ".join(data) + ")"
        self.db.execute(cmd)
        return True

    def insert_team_bans(self, teamBans: List[object], teamId: int, gameId: int) -> bool:
        """ TODO: Implement, TeamBansDto """
        return False
        if not teamBans:
            return

        cols = [
            "pickTurn",
            "championId"
        ]

        for teamBan in teamBans:
            start_cmd = "INSERT INTO TeamBansDto VALUES (" + str(gameId) + "," + str(teamId)
            for col in cols:
                try:
                    start_cmd += ", " + teamBan[col]
                except:
                    start_cmd += ", null"
            cmd = start_cmd + ")"
            self.db.execute(cmd)
        return True

    def insert_team_stats(self, teamstats: List[object], gameId: int) -> None:
        """ TeamStatsDto and TeamBansDto """
        cols = [
            "firstDragon",
            "firstInhibitor",
            "baronKills",
            "firstRiftHerald",
            "firstBaron",
            "riftHeraldKills",
            "firstBlood",
            "teamId",
            "firstTower",
            "vilemawKills",
            "inhibitorKills",
            "towerKills",
            "dominionVictoryScore",
            "win",
            "dragonKills",
        ]
        quoted_cols = ["'" + col + "'" for col in cols]
        for team in teamstats:
            teamId = team['teamId']
            cmd = "INSERT INTO TeamStatsDto (" + ", ".join(["'gameId'"] + quoted_cols) + ") VALUES ("
            cmd += str(gameId)
            for col in cols:
                cmd += ", '{}'".format(team[col])
            cmd += ")"
            self.insert_team_bans(team['bans'], teamId, gameId)
            self.db.execute(cmd)

    def insert_participant_timeline(self, participant: object, gameId: int) -> bool:
        """ TODO: Implement """
        return True

    def insert_participant_stats(self, participant: object, gameId: int) -> bool:
        """ TODO: Implement """
        return True

    def insert_participants(self, participants: List[object], gameId: int) -> bool:
        """ ParticipantDto """
        cols = [
            "participantId",
            "runes",
            "teamId",
            "spell2Id",
            "masteries",
            "highestAchievedSeasonTier",
            "spell1Id",
            "championId",
        ]
        for participant in participants:
            start_cmd = "INSERT INTO ParticipantDto " \
                        "VALUES " \
                        "(" + str(gameId) + ", "
            data = []
            for col in cols:
                try:
                    datum = "'{}'".format(participant[col])
                except:
                    datum = "'null'"
                data.append(datum)
            cmd = start_cmd + ", ".join(data) + ")"
            self.db.execute(cmd)
            self.insert_participant_stats(participant, gameId)
            self.insert_participant_timeline(participant, gameId)
        return True

    def insert_player(self, player: Dict, gameId: int, participantId: int) -> bool:
        """ PlayerDto """
        cols = [
            "currentPlatformId",
            "summonerName",
            "matchHistoryUri",
            "platformId",
            "currentAccountId",
            "profileIcon",
            "summonerId",
            "accountId"
        ]
        col_name = ", ".join([*["'gameId'", "'participantId'"], *["'" + col + "'" for col in cols]])
        start_cmd = "INSERT INTO PlayerDto " \
                    "(" + col_name + ") " \
                    "VALUES (" + str(gameId) + ", " + \
                    str(participantId) + ", "
        data = []
        for col in cols:
            try:
                datum = "'" + str(player[col]) + "'"
            except:
                datum = "'null"
            data.append(datum)
        cmd = start_cmd + ", ".join(data) + ")"
        self.db.execute(cmd)
        return True

    def insert_participant_identities(self, participantIdentities: List[Dict], gameId: int) -> None:
        """ ParticipantIdentityDto, PlayerDto """
        for participantIdentity in participantIdentities:
            self.insert_player(participantIdentity['player'], gameId, participantIdentity['participantId'])

    def handle_participant_frames(self, pFrames: Dict[str, Dict], gameId: int, timestamp: int):
        cols = [
            "participantId",
            "currentGold",
            "totalGold",
            "level",
            "xp",
            "minionsKilled",
            "jungleMinionsKilled"
        ]
        for k, pframe in pFrames.items():
            cmd = "INSERT INTO ParticipantFrame VALUES ("
            cmd += str(gameId)
            cmd += ", " + str(timestamp) + ", "
            data = []
            for p in ['x', 'y']:
                try:
                    datum = pframe['position'][p]
                except:
                    datum = 'null'
                data.append(datum)
            for col in cols:
                try:
                    datum = pframe[col]
                except:
                    datum = 'null'
                data.append(datum)
            cmd += ", ".join([str(d) for d in data]) + ")"
            print(cmd)
            self.db.execute(cmd)

    def handle_events(self, events: List[Dict], gameId: int):
        cols = [
            "timestamp",
            "x",
            "y",
            "killerId",
            "victimId",
            "participantId",
            "itemId"
        ]
        for event in events:
            cmd = "INSERT INTO Events VALUES ("
            cmd += str(gameId)
            cmd += ", '" + event['type'] + "', "
            data = []
            for col in cols:
                try:
                    datum = event[col]
                except:
                    datum = 'null'
                data.append(datum)
            cmd += ", ".join([str(d) for d in data]) + ")"
            self.db.execute(cmd)

    def handle_frame(self, frame: Dict, gameId: int):
        timestamp = frame['timestamp']
        participantFrames = frame['participantFrames']
        events = frame['events']
        self.handle_participant_frames(participantFrames, gameId, timestamp)
        self.handle_events(events, gameId)

    def handle_timeline(self, timeline: Dict, gameId: int) -> None:
        cmd = "INSERT INTO Timelines VALUES ("
        cmd += str(gameId)
        cmd += ", " + str(timeline['frameInterval'])
        cmd += ", " + str(len(timeline['frames'])) + ")"
        self.db.execute(cmd)
        frames = timeline['frames']
        for frame in frames:
            self.handle_frame(frame, gameId)

    def handle_match(self, match_id: int) -> None:
        self.logger.info("--- Match {} ---".format(str(match_id)))
        match = self.riot.getMatch(match_id)
        self.insert_match_data(match)

        team_stats = match['teams']
        self.insert_team_stats(team_stats, match_id)

        participants = match['participants']
        self.insert_participants(participants, match_id)

        participant_identities = match['participantIdentities']
        self.insert_participant_identities(participant_identities, match_id)

        self.logger.info("--- Match Timeline {} ---".format(str(match_id)))
        matchTimeline = self.riot.getTimeline(match_id)
        self.handle_timeline(matchTimeline, match_id)

        self.db.commit()



if __name__ == "__main__":
    riot_key = "RGAPI-48aed195-b319-4954-86ad-a58352ce2c01"
    seed_player = 50068799  # "Faker"
    db_name = "data/lolmatch.db"

    matchcrawler = MatchCrawler(api_key=riot_key, dbname=db_name)
    matchcrawler.crawl(seed_player)
