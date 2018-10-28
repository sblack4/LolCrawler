"""
sql for tables corresponding to definitions in swagger file
match-v3.
- ParticipantIdentityDto
- PlayerDto
- TeamStatsDto
- TeamBansDto
- ParticipantDto
- ParticipantStatsDto
- RuneDto
- ParticipantTimelineDto
- MasterDto
- MatchlistDto
- MatchReferenceDto
- MatchTimelineDto
- MatchFrameDto
- MatchParticipantDto
- MatchPositionDto
- MatchEventDto

It's not fully implemented but will give you the structure of your tables

"""

from pyswagger import App
from pyswagger.spec.v2_0.objects import Schema
from typing import Dict
# from sqlalchemy import create_engine


class LolSchema(Schema):
    """the riot api has some other properties"""
    def __init__(self):
        super(Schema, self).__init__()
        self.type = str()


class LolSql(object):
    def __init__(self, swagger_file: str="swaggerspec-2.0.yml"):
        self.app = App.create(swagger_file)
        self.definitions: Dict = self.app.root.resolve("definitions")
        # self.engine = create_engine('sqlite:///Users/DV79FN/Git/lolcrawler/data/lolsql.db')

    def create_tables(self, definition_list: str, definition_name: str, *argv):
        dto: Dict = self.definitions[definition_list + "." + definition_name].properties
        attributes = [*argv] if argv else []
        create_tables = []
        for k, v in dto.items():
            # arrays will need to be new tables
            if v.type == 'array':
                pass
                # create new table for them?
                new_dto = v._children_['items'].dump()['$ref'].split('.')[-1]
                new_keys = [x for x in argv] + [definition_name]
                create_tables += self.create_tables(definition_list, new_dto, *new_keys)
            attributes.append(k)
        create_table = "CREATE TABLE " + definition_name + " ( " + ", ".join(attributes) + ")"
        create_tables.append(create_table)
        return create_tables


if __name__ == "__main__":
    lolsql = LolSql()

    print("if you're calling the matches endpoint, you'll get a MatchDto")
    definition_list = 'match-v3'
    matches = 'MatchDto'
    create_tables = lolsql.create_tables(definition_list, matches)
    for c in create_tables:
        print(c)

    print("likewise for the MatchTimelineDto")
    matches = 'MatchTimelineDto'
    create_tables = lolsql.create_tables(definition_list, matches)
    for c in create_tables:
        print(c)
