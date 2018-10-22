"""

"""
from lolcrawler import LolCrawler


class TimeLineCrawler(LolCrawler):
    def handle_match(self, match_id: int):
        match = self.riot.getMatch(match_id)
        self.handle_participants(match)
        timeline = self.riot.getTimeline(match["gameId"])



if __name__ == "__main__":
    riot_key = "RGAPI-aa4df822-5310-4608-a56f-8d8a955b3729"
    db_name = "loltimeline.db"

    timelinecrawler = TimeLineCrawler(api_key=riot_key, dbname=db_name)
    timelinecrawler.crawl()