import requests
import pandas as pd
from ratelimit import limits, sleep_and_retry
from datetime import date
import time
import os
import csv 
import json
from tqdm import tqdm

class Summoner:
    def __init__(self, api_key, server):
        self.api_key = api_key
        self.server = server
        self.base_url = f"https://{self.server}.api.riotgames.com/tft/"
        if server == 'na1':
            self.region = 'americas'
        elif server == 'kr':
            self.region = 'asia'
        else:
            self.region = 'europe'
        self.base_url2 = f"https://{self.region}.api.riotgames.com/tft/match/v1/matches/"
        self.headers = {
            "X-Riot-Token": self.api_key,
        }
    
        self.data_dir = "data"
        self.today_dir = os.path.join(self.data_dir, str(date.today()))
        self.server_dir = os.path.join(self.today_dir, self.server)
        self.create_directories()
        
    def create_directories(self):
        os.makedirs(self.today_dir, exist_ok=True)
        os.makedirs(self.server_dir, exist_ok=True)
    
    @sleep_and_retry
    @limits(calls=100, period=125)
    def check_limit(self):
        return
    
    def puuid(self, entries):
        ids = []
        sum_id = []
        
        leagues = ['DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER']
        tiers = ['I', 'II', 'III', 'IV']
        
        for league in leagues:
            for tier in tiers:
                url = f'{self.base_url}league/v1/entries/{league}/{tier}?queue=RANKED_TFT&page=1'
                json_data = self.call(url)[:entries]
                for entry in json_data:
                    ids.append(entry['puuid'])
                    sum_id.append(entry['summonerId'])
        
        filename = os.path.join(self.server_dir, "puuid.csv")
        rows = zip(sum_id, ids)
        with open(filename, mode='w', newline='') as file:
            
            writer = csv.writer(file)
            writer.writerow(['summoner_id', 'puu_id']) 
            writer.writerows(rows)
        
    def matches(self, days):
        end = int(time.time())
            
        start = end - int(days* 86400)
            
        ids = []
        with open(f'{self.server_dir}/puuid.csv','r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ids.append(row[1])
        filename = os.path.join(self.server_dir, "matches.csv")

        
        for id in tqdm(ids, desc = self.server, leave = True):
            url = f'{self.base_url2}by-puuid/{id}/ids?endTime={end}&startTime={start}'
            data = self.call(url)
            match_ids = [id for id in data]
                
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                for id in match_ids:
                    writer.writerow([id])
    
    def data(self, match_id):
        url = f'{self.base_url2}{match_id}'
        data = self.call(url)
        return data
    
    def write(self, data, filename):
        filepath = f'{self.today_dir}/{filename}.json'
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    def run(self):
        ids = []
        with open(f'{self.server_dir}/matches.csv','r') as f:
            reader = csv.reader(f)
            for row in reader:
                ids.append(row[0])
        
        for id in tqdm(ids, desc = self.server, leave = True):
            filepath = f'{self.today_dir}/{id}.json'
            if not os.path.exists(filepath): 
                data = self.data(id)
                self.write(data, id)

        
            
    def call(self, url):
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                self.check_limit()
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    retries += 1
                    time.sleep(5)  # Wait for 5 seconds before retrying
            except requests.exceptions.RequestException as e:
                retries += 1
                time.sleep(5)  # Wait for 5 seconds before retrying

        raise Exception("Max retries exceeded. Unable to make API call.")

    
# Usage example:
"""api_key = "RGAPI-804fd993-086e-4742-95af-349b063ae286"
region = "na1"
summoner = Summoner(api_key, region)
summoner.run()"""