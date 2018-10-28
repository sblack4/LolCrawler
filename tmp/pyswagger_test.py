from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose
from typing import Dict

# load Swagger resource file into App object

app = App.create("lolcrawler/swaggerspec-2.0.yml")

definitions: Dict = app.root.resolve("definitions")
for k, v in definitions.items():
    print(k, v)

auth = Security(app)
auth.update_with('api_key', 'RGAPI-8dc9be1b-5b2a-4db5-8cb6-66ec939033e8')

# init swagger client
client = Client(auth)

foo = app.resolve('#/definitions/match-v3.MatchDto')
print(foo)

for i in range(60):
    # - access an Operation object via App.op when operationId is defined
    req, resp = app.op['getBySummonerName'](summonerName="Faker")
    # prefer json as response
    req.produce('application/json')
    faker = client.request((req, resp))

    print(faker.header)
    print(faker.data)
    print(faker.raw)
    print(faker.status)
    print("-----")
