import requests
import asyncio
import aiohttp
from tqdm.asyncio import tqdm
import time
import pandas as pd

API_KEY = 'RGAPI-c64d4d35-f33e-4cc6-8e5a-cee23e6654e3' #store your riot developer api key here
REGION = 'na1' # store your region code, i.e north america stands for na1
MATCH_REGION = 'americas'
matchIDS = []

def get_puuid(SummonerID):
    url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/{SummonerID}?api_key={API_KEY}'
    response = requests.get(url)
    if(response.status_code == 200):
        return response.json()['puuid']
    else:
        print(f"Failed to fetch PUUID for SummonerID {SummonerID}: {response.status_code}")
        return []
    

def get_match_ids(puuid, type = "ranked", count = 100):
    url = f'https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={type}&start=0&count={count}&api_key={API_KEY}'
    response = requests.get(url)
    if(response.status_code == 200):
        return response.json()
    else:
        print(f"Failed to fetch match IDs for PUUID {puuid}: {response.status_code}")
        return []

def fetch_puuids_and_match_ids(summoner_list):
    for summoner_dict in tqdm(summoner_list, desc="Updating Summoner Data", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [%]"):
        puuid = get_puuid(summoner_dict['summonerId'])
        if(puuid):
            summoner_dict['puuid'] = puuid
            match_list = get_match_ids(puuid)
            for match in match_list:
                if match not in matchIDS:
                    matchIDS.append(match)
        time.sleep(1)
    return summoner_list
        
def save_matchIDS_to_csv(matchIDS_list):
    df = pd.DataFrame(matchIDS, columns = ["Match ID"])
    file_name = "NA_MatchIDs.csv"
    df.to_csv(f"{file_name}", index=False)
    print(f"Saved {len(matchIDS)} Match Ids to '{file_name}'.")

def collect_master_players_info():
    url = f'https://{REGION}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}'
    while True:
        response = requests.get(url)
        if(response.status_code == 200):
            all_master_players = response.json()['entries']
            total_players = len(all_master_players)
            
            with tqdm(total=100, desc="Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [%]") as progress_bar:
                for i, player in enumerate(all_master_players):
                    progress_percentage = (i+1) / total_players * 100
                    progress_bar.update(progress_percentage - progress_bar.n)
            print(f"Collected {len(all_master_players)} players from Master rank.")
            return all_master_players
        elif(response.status_code == 429):
            retry_time = 10
            print(f"Rate limit exceeded, retrying after {retry_time} seconds...")
            time.sleep(retry_time)
            continue
        else:
            print(f"Error Fetching Master Players: {response.status_code}")
            return None


def collect_grandMaster_players_info():
    url = f'https://{REGION}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}'
    while True:
        response = requests.get(url)
        if(response.status_code == 200):
            all_grandMaster_players = response.json()['entries']
            total_players = len(all_grandMaster_players)
            
            with tqdm(total=100, desc="Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [%]") as progress_bar:
                for i, player in enumerate(all_grandMaster_players):
                    progress_percentage = (i+1) / total_players *100
                    progress_bar.update(progress_percentage - progress_bar.n)
            print(f"Collected {len(all_grandMaster_players)} players from GrandMaster Rank.")
            return all_grandMaster_players
        elif(response.status_code == 429):
            retry_time = 10
            print(f"Rate limit exceeded, retrying after {retry_time} seconds...")
            time.sleep(retry_time)
            continue
        else:
            print(f"Error Fetching GrandMaster Players: {response.status_code}")
            return []
            
def collect_challenger_players_info():
    url = f'https://{REGION}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}'
    while True:
        response = requests.get(url)
        if(response.status_code == 200):
            all_challenger_players = response.json()['entries']
            total_players = len(all_challenger_players)
            with tqdm(total=100, desc="Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [%]") as progress_bar:
                for i, player in enumerate(all_challenger_players):
                    progress_percentage = (i+1) / total_players * 100
                    progress_bar.update(progress_percentage - progress_bar.n)
            print(f"Collected {len(all_challenger_players)} players from Challenger Rank.")
            return all_challenger_players
        elif(response.status_code == 429):
            retry_time = 10
            print(f"Rate limit exceeded, retry after {retry_time} seconds...")
            time.sleep(10)
            continue
        else:
            print(f"Error Fetching Challenger Players: {response.status_code}")
            return []
master_players = collect_master_players_info()
grandMaster_players = collect_grandMaster_players_info()
challenger_players = collect_challenger_players_info()

master_players = fetch_puuids_and_match_ids(master_players)
grandMaster_players = fetch_puuids_and_match_ids(grandMaster_players)
challenger_players = fetch_puuids_and_match_ids(challenger_players)

save_matchIDS_to_csv(matchIDS)

# Convert lists to DataFrames
master_df = pd.DataFrame(master_players)
grandMaster_df = pd.DataFrame(grandMaster_players)
challenger_df = pd.DataFrame(challenger_players)




# Save each DataFrame to a separate sheet in an Excel file
with pd.ExcelWriter('league_of_legends_players.xlsx') as writer:
    if not master_df.empty:
        master_df.to_excel(writer, sheet_name='Master', index=False)
    if not grandMaster_df.empty:
        grandMaster_df.to_excel(writer, sheet_name='Grandmaster', index=False)
    if not challenger_df.empty:
        challenger_df.to_excel(writer, sheet_name='Challenger', index=False)

print(f"All data saved to 'league_of_legends_players.xlsx'.")