from tftskill.summoner import Summoner
from concurrent.futures import ThreadPoolExecutor

regions = ['na1', 'kr', 'euw1']

api_key = "RGAPI-804fd993-086e-4742-95af-349b063ae286"

def get_data(api_key, region):
    summoner = Summoner(api_key, region)
    summoner.run()

with ThreadPoolExecutor(max_workers=len(regions)) as executor:
    for region in regions:
        executor.submit(get_data, api_key, region)