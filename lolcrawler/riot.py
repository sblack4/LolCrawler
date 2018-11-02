import json
import requests
from requests import Response
from time import sleep
from typing import Union, Dict
import logging


logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    """basic exception """
    pass


class Riot:
    """
    this class makes it easy to call the riot api
    and handles the rate limit exceptions when you call too often
    """
    routes: Dict[str, str]

    def __init__(self, api_key):
        self.api_key = api_key
        self.api_arg = "?api_key=" + api_key
        self.url_base = "https://na1.api.riotgames.com"
        self.routes = {
            "matches": "/lol/match/v3/matches",
            "summoners/by-name": "/lol/summoner/v3/summoners/by-name",
            "matchlist": "/lol/match/v3/matchlists/by-account",
            "featuredMatches": "/lol/spectator/v3/featured-games",
            "timeline": "/lol/match/v3/timelines/by-match"
        }

    def badStatus(self, response: Response) -> bool:
        """
        returns true if the rate limit has been hit
        otherwise it returns false
        :param response:
        :return:
        """
        status_code = response.status_code
        if status_code == 200:
            return False
        elif status_code == 429:  # Rate Limit
            return True
        elif status_code == 403:
            raise Exception('YOUR AUTH TOKEN EXPIRED! Response 403: ' + response.text)
        else:
            logger.warning("Status code error:{} ".format(status_code), response)
        return False

    def getUrl(self, endpoint: str, arg: Union[str, int]) -> str:
        return self.url_base + self.routes[endpoint] + "/" + str(arg) + self.api_arg

    def getMatchList(self, account_id: Union[str, int]) -> json:
        url = self.getUrl("matchlist", account_id)
        response = requests.get(url)
        if self.badStatus(response):
            sleep(60)
            return self.getMatchList(account_id)
        return response.json()

    def getSummonerByName(self, name: str) -> json:
        url = self.getUrl("summoners/by-name", name)
        response = requests.get(url)
        if self.badStatus(response):
            sleep(60)
            return self.getSummonerByName(name)
        return response.json()

    def getMatch(self, id: Union[int, str]) -> json:
        url = self.getUrl("matches", id)
        response: Response = requests.get(url)
        if self.badStatus(response):
            sleep(60)
            return self.getMatch(id)
        return response.json()

    def getFeaturedMatches(self) -> json:
        url = self.url_base + self.routes["featuredMatches"] + self.api_arg
        response = requests.get(url)
        if self.badStatus(response):
            sleep(60)
            return self.getFeaturedMatches()
        return response.json()

    def getRoute(self, route: str, arg: str="") -> json:
        arg = "/" + str(arg) if arg else ""
        url = self.url_base + self.routes[route] + arg + self.api_arg
        response = requests.get(url)
        if self.badStatus(response):
            sleep(60)
            return self.getRoute(route)
        return response.json()

    def getTimeline(self, match_id: int) -> json:
        route = "timeline"
        return self.getRoute(route=route, arg=str(match_id))

if __name__ == "__main__":
    key = "RGAPI-eb49c30b-3d29-4160-a19a-3ab744f48aa0"
    api = Riot(key)

    players = [
        'Faker',
        'Westdoor',
        'Marin',
        'ssumday',
        'huni',
        'bjergsen',
        'ziv',
        'aphromoo',
        'piccaboo',
        'bang',
        'doublelift',
        'pawn',
        'clearlove',
        'yellowstar',
        'deft',
        'pyl',
        'rookie',
        'kakao',
        'imp'
    ]
    for i in range(100):
        print(api.getFeaturedMatches())

