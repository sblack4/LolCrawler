import json
import requests
from requests import Response
from time import sleep
from typing import Union, Dict
from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose
from pyswagger.primitives._model import Model
import logging


logger = logging.getLogger(__name__)


class SwaggerResponse(Model):
    """abstract class"""
    pass

# class SwaggerResponse(object):
#     """abstract class"""
#     def __init__(self):
#         self.data = dict()
#         self.header = dict()
#         self.raw = bytes()
#         self.status = int()


class RateLimitException(Exception):
    """basic exception """
    pass


class Riot:

    def __init__(self,
                 api_key: str,
                 swagger_file: str="http://www.mingweisamuel.com/riotapi-schema/swaggerspec-2.0.yml"):

        self.api_key = api_key
        self.swagger_file = swagger_file
        self.app = App.create(swagger_file)
        self.auth = Security(self.app)
        self.auth.update_with("api_key", api_key)
        self.client = Client(self.auth)

    @staticmethod
    def badStatus(response: SwaggerResponse) -> bool:
        status_code = response.status
        good_statuses = [200]
        if status_code in good_statuses:
            return True
        elif status_code == 429:  # Rate Limit
            # raise RateLimitException("rate limit hit ")
            return True
        elif status_code == 403:
            raise Exception('YOUR AUTH TOKEN EXPIRED! Response 403: ' + response.text)
        return False

    def get_opp(self, operation_id: str, **kwargs) -> SwaggerResponse:
        print(kwargs)
        req, resp = self.app.op[operation_id](**kwargs)
        req.produce('application/json')
        response: SwaggerResponse = self.client.request((req, resp))
        if response.status == 429:
            logger.warning("rate limit hit")
            sleep(60)
            return self.client.request((req, resp))
        return response

    def getMatchList(self, account_id: Union[str, int]) -> json:
        operation_id = 'getMatchlist'
        response = self.get_opp(operation_id, accountId=account_id)
        return response.data

    def getSummonerByName(self, name: str) -> json:
        operation_id = 'getBySummonerName'
        response = self.get_opp(operation_id, summonerName=name)
        return response.data

    def getMatch(self, matchId: Union[int, str]) -> json:
        op_id = 'getMatch'
        response = self.get_opp(op_id, matchId=matchId)
        return response.data

    def getFeaturedGames(self) -> json:
        op_id = 'getFeaturedGames'
        response = self.get_opp(op_id)
        return response.data

    def getMatchTimeline(self, match_id: int) -> json:
        op_id = 'getMatchTimeline'
        response = self.get_opp(op_id, matchId=match_id)
        return response.data


if __name__ == "__main__":
    key = "RGAPI-8dc9be1b-5b2a-4db5-8cb6-66ec939033e8"
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

    for p in players:
        playa = api.getSummonerByName(p)
        print(playa)
        print(type(playa))
