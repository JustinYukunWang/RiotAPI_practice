import requests
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "RGAPI-0552d49e-1fb0-4807-a505-34ed938ecc63"  # needs to be updated everytime we log in 
REGION = "americas"

def get_puuid_using_riotID(gameID, tag):
    proper_ID = urllib.parse.quote(gameID)  # Change the ID and the tag into url-legal format
    proper_tag = urllib.parse.quote(tag)
    puuid_fetch_url = (f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{proper_ID}/{proper_tag}?api_key={API_KEY}")
    resp = requests.get(puuid_fetch_url).json()
    puuid = resp['puuid']
    return puuid

def get_match_history(puuid):
    player_matchHistory_fetch_url = (f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=20&api_key={API_KEY}")
    matchData = requests.get(player_matchHistory_fetch_url).json()
    return matchData

def get_match_details(match_id):
    match_data_fetch_url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    temp_MatchData = requests.get(match_data_fetch_url).json()
    return temp_MatchData

def get_aThousand_matches(player_puuid, matchData):
    matchData += get_match_history(player_puuid)
    player_list = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_match_details, match) for match in matchData]
        for future in as_completed(futures):
            temp_MatchData = future.result()
            player_list += temp_MatchData["metadata"]["participants"]  # This is a list of PUUIDs of players in that game
    
    unique_players = set(player_list)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_match_history, player) for player in unique_players]
        for future in as_completed(futures):
            matchData += future.result()
    
    return matchData

puuid = get_puuid_using_riotID("Voli StormValhir", "NA1")
print("Running...")
matchData = []
matchData = list(set(get_aThousand_matches(puuid, matchData)))

print(len(matchData))

with open("matchID(Plat-Emerald)1.txt", "w") as outfile:
    outfile.write("\n".join(matchData))
    outfile.close()
