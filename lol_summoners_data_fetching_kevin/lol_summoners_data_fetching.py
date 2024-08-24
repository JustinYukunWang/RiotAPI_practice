import requests
from tqdm import tqdm
import time
import pandas as pd

API_KEY = 'RGAPI-86fd201a-4c34-4c31-b2d7-bbf5f87a7f99' #store your riot developer api key here
REGION = 'na1' # store your region code, i.e north america stands for na1


def get_diamond_players_info_by_disivion(division, page=1):
    '''
    this function returns a list where each element is a dictionary containing player's data
    i.e:{
        "leagueId": "0a7e58a5-145b-40f0-abe7-5c4b1fcfc540",
        "queueType": "RANKED_SOLO_5x5",
        "tier": "DIAMOND",
        "rank": "IV",
        "summonerId": "w9g1K4pjs1XQSVwAycxArZwN1crWmb0Bq0HaRaZcBAc08zZ_",
        "leaguePoints": 0,
        "wins": 37,
        "losses": 23,
        "veteran": false,
        "inactive": false,
        "freshBlood": false,
        "hotStreak": false
    }
    '''
    url = f'https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/{division}?page={page}&api_key={API_KEY}'
    while True:
        response = requests.get(url)
        
        if(response.status_code == 200): #request successfully we return the data
            return response.json()
        elif (response.status_code == 429): # rate time exceeded
            retry_time = 10;
            print(f"Rate limit exceeded retrying after {retry_time} seconds...")
            time.sleep(retry_time)
        else:
            print(f"Error fetching Diamond {division} on page{page}: {response.status_code}")
            return []




def collect_diamond_players_info():
    all_diamond_players = []
    for division in ['I', 'II', 'III', 'IV']:
        page = 1
        with tqdm(desc=f'Fetching Diamond {division} players', unit='player') as progress_bar:
            while True:
                players = get_diamond_players_info_by_disivion(division, page=page)
                if players:
                    all_diamond_players.extend(players)
                    progress_bar.update(len(players))
                    page += 1
                    time.sleep(1)
                else:
                    break
    print(f"\nCollected {len(all_diamond_players)} players from Diamond rank.")
    return all_diamond_players

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