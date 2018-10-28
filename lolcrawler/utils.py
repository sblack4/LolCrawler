import json
import logging
from typing import Dict


def write_json(json_obj, filename: str) -> None:
    try:
        with open(filename, 'w+') as fh:
            fh.write(json.dumps(json_obj, indent=2))
    except Exception as ex:
        logging.error(ex)


def getSomething(dic: Dict, k: str):
    retx= "0"
    rety= "0"
    try:
        retx = dic[k]["0-10"]
        rety = dic[k]['10-20']
    except Exception as e:
        logging.warning(e)
    return retx, rety


def get_participant_wins(match: Dict) -> Dict:
    """ given list of participants returns a dict of participantId -> win
    https://cassiopeia.readthedocs.io/en/latest/cassiopeia/match.html#cassiopeia.core.match.Participant
    :return:
    """
    participant_list = match['participants']
    participant_list.sort(key=id)
    return {x['participantId']: x['stats']['win'] for x in participant_list}

