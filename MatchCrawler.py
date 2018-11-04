"""
runs the MatchCrawler for infinity
and inserts the data to the database
see
https://developer.riotgames.com/api-methods/#match-v3/GET_getMatch
https://developer.riotgames.com/api-methods/#match-v3/GET_getMatchTimeline

"""
from typing import List, Dict
from lolcrawler.lolcrawler import LolCrawler


class MatchCrawler(LolCrawler):
    """
    LolCrawler takes in the matchlist of a player,
    and iterates new players
    MatchCralwer takes that one match and has the logic
    to transform the json into sql statements
    it does this for Match data and Timeline data for each match
    to insert it into a sqllite database see loldb.py, it's a facade over the db
    """
    # no init because there is an init in the parent class

    def insert_match_data(self, match: Dict) -> bool:
        """
        turns the match values into and inset statement for the MatchDto table
        :param match:
        :return:
        """
        # the columns I want
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
            # try to get the data from the match object
            try:
                # use quotes because they are text values in the database
                datum = "'" + str(match[col]) + "'"
            except Exception as ex:
                self.logger.warning(ex)
                # if it's missing an error gets thrown so mark it as null
                datum = "'null'"
            # add that datum to the list
            data.append(datum)
        # turn the start of the insert statement and the values into a SQL statement
        cmd = start_cmd + ", ".join(data) + ")"
        # execute the SQL
        self.db.execute(cmd)
        return True

    def insert_team_bans(self, teamBans: List[object], teamId: int, gameId: int) -> bool:
        """ TODO: Implement, TeamBansDto
        this was throwing errors and there usually aren't any bans
        """
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

    def insert_team_stats(self, teamstats: List[Dict], gameId: int) -> None:
        """
        inserts data into the TeamStatsDto and TeamBansDto tables
        TeamStatsDto is the name of the object from the API
        https://developer.riotgames.com/api-methods/#match-v3/GET_getMatch
        """
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
        """ TODO: Implement
        has summary stats about particpant timelines
        """
        return True

    def insert_participant_stats(self, participant: object, gameId: int) -> bool:
        """ TODO: Implement
        more stats about the participants game play
        """
        return True

    def insert_participants(self, participants: List[Dict], gameId: int) -> bool:
        """ insert data into ParticipantDto given a list of them"""
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
        # a new row for every participant
        for participant in participants:
            start_cmd = "INSERT INTO ParticipantDto " \
                        "VALUES " \
                        "(" + str(gameId) + ", "
            data = []
            for col in cols:
                try:
                    datum = "'{}'".format(participant[col])
                except Exception as ex:
                    self.logger.warning(ex)
                    datum = "'null'"
                data.append(datum)
            cmd = start_cmd + ", ".join(data) + ")"
            self.db.execute(cmd)
            self.insert_participant_stats(participant, gameId)
            self.insert_participant_timeline(participant, gameId)
        return True

    def insert_player(self, player: Dict, gameId: int, participantId: int) -> bool:
        """ inserts into table PlayerDto - has the player's account data and stuff """
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
        # fancy way to get list of column names
        col_name = ", ".join([*["'gameId'", "'participantId'"], *["'" + col + "'" for col in cols]])

        # the start of the command
        # and the first few values that are numbers so don't need quotes
        start_cmd = "INSERT INTO PlayerDto " \
                    "(" + col_name + ") " \
                    "VALUES (" + str(gameId) + ", " + \
                    str(participantId) + ", "
        data = []
        # try to get the data like before
        for col in cols:
            try:
                datum = "'" + str(player[col]) + "'"
            except Exception as ex:
                self.logger.warning(ex)
                datum = "'null"
            data.append(datum)
        # make it into one command and insert into the database
        cmd = start_cmd + ", ".join(data) + ")"
        self.db.execute(cmd)
        return True

    def insert_participant_identities(self, participantIdentities: List[Dict], gameId: int) -> None:
        """ hands data off to be inserted into ParticipantIdentityDto, PlayerDto """
        for participantIdentity in participantIdentities:
            self.insert_player(participantIdentity['player'], gameId, participantIdentity['participantId'])

    def handle_participant_frames(self, pFrames: Dict[str, Dict], gameId: int, timestamp: int):
        """
        goes through the participant frames and inserts each one as a row into the ParticipantFrame table
        :param pFrames:
        :param gameId:
        :param timestamp:
        :return:
        """
        cols = [
            "participantId",
            "currentGold",
            "totalGold",
            "level",
            "xp",
            "minionsKilled",
            "jungleMinionsKilled"
        ]
        # because pFrames is a Dict use .items() to go through each key, value pair
        for k, pframe in pFrames.items():
            cmd = "INSERT INTO ParticipantFrame VALUES ("
            cmd += str(gameId)
            cmd += ", " + str(timestamp) + ", "
            data = []
            # the same try except stuff but for the position data and for all the other data
            # the position data is nested so it needs to be treated differently
            for p in ['x', 'y']:
                try:
                    datum = pframe['position'][p]
                except:
                    datum = 'null'
                data.append(datum)
            # all the other columns
            for col in cols:
                try:
                    datum = pframe[col]
                except Exception as ex:
                    self.logger.warning(ex)
                    datum = 'null'
                data.append(datum)
            # finally make one command and insert it
            cmd += ", ".join([str(d) for d in data]) + ")"
            self.db.execute(cmd)

    def handle_events(self, events: List[Dict], gameId: int):
        """
        inserts events from the timeline to the Events table
        :param events:
        :param gameId:
        :return:
        """
        cols = [
            "killerId",
            "victimId",
            "participantId",
            "itemId"
        ]
        # events is a list so there will be a new row for each
        for event in events:
            cmd = "INSERT INTO Events VALUES ("
            cmd += str(gameId) + ", '"
            cmd += event['type'] + "', '"
            cmd += str(event['timestamp']) + "', "
            data = []
            try:
                data.append(event['position']['x'])
                data.append(event['position']['y'])
            except Exception as ex:
                self.logger.warning(ex)
                data.append('null')
                data.append('null')
            for col in cols:
                try:
                    datum = event[col]
                except Exception as ex:
                    self.logger.warning(ex)
                    datum = 'null'
                data.append(datum)
            cmd += ", ".join([str(d) for d in data]) + ")"
            self.db.execute(cmd)

    def handle_frame(self, frame: Dict, gameId: int):
        """
        handles the frames from the timeline
        it passes them to other functions to be inserted
        :param frame:
        :param gameId:
        :return:
        """
        timestamp = frame['timestamp']
        participantFrames = frame['participantFrames']
        events = frame['events']
        self.handle_participant_frames(participantFrames, gameId, timestamp)
        self.handle_events(events, gameId)

    def handle_timeline(self, timeline: Dict, gameId: int) -> None:
        """
        inserts data about the overall timeline into Timelines
        and passes the data off to be inserted
        :param timeline:
        :param gameId:
        :return:
        """
        cmd = "INSERT INTO Timelines VALUES ("
        cmd += str(gameId)
        cmd += ", " + str(timeline['frameInterval'])
        cmd += ", " + str(len(timeline['frames'])) + ")"
        self.db.execute(cmd)
        frames = timeline['frames']
        for frame in frames:
            self.handle_frame(frame, gameId)

    def handle_match(self, match_id: int) -> None:
        """
        the first thing that gets called
        after you call crawl
        it takes the match id and gets all the match data from the riot API
        then it breaks the data apart and sends it to other methods to be inserted
        then it gets the match timeline and passes that to be inserted to
        :param match_id:
        :return:
        """
        self.logger.info("--- Match {} ---".format(str(match_id)))

        # get the data from riot API
        match = self.riot.getMatch(match_id)

        # insert overall match data
        self.insert_match_data(match)

        # get and insert team data
        team_stats = match['teams']
        self.insert_team_stats(team_stats, match_id)

        # get and insert participant data
        participants = match['participants']
        self.insert_participants(participants, match_id)

        participant_identities = match['participantIdentities']
        self.insert_participant_identities(participant_identities, match_id)

        # get and insert timeline data
        self.logger.info("--- Match Timeline {} ---".format(str(match_id)))
        matchTimeline = self.riot.getTimeline(match_id)
        self.handle_timeline(matchTimeline, match_id)

        # committing saves all our changes in the database
        self.db.commit()



if __name__ == "__main__":
    # this gets called when you run this file

    riot_key = "RGAPI-edefd6ca-2c91-4f60-bdfd-94b5de163061"
    seed_player = 50068799  # "Faker"

    # in the data folder
    db_name = "data/lolmatch.db"

    # create matchcrawler object and start crawling
    matchcrawler = MatchCrawler(api_key=riot_key, dbname=db_name)
    matchcrawler.crawl(seed_player)



