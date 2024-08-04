import requests
import json

API_KEY = "RGAPI-e471da40-80fd-4dc5-be05-dbf7dde1b7be"#needs to be updated everytime we log in

#fetch the puuid inorder to fetch the player info later USING: account: account by riot ID
puuid_fetch_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Voli%20StormValhir/NA1?api_key=" + API_KEY
resp = requests.get(puuid_fetch_url).json()
puuid = resp['puuid']

#fetching player information using puuid 
player_info_fetch_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/2IPkTfIvLAU3O9UZzwENXmJOXnyFESoDK6tf4OW9_-dvgqc9AyQflo3MqDQzccDxFN8-focd7JbuLQ?api_key=" + API_KEY
player_info = requests.get(player_info_fetch_url).json()


player_matchHistory_fetch_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=20&api_key=" +  API_KEY
matchData = requests.get(player_matchHistory_fetch_url).json()





with open("matchData.txt", "w") as outfile:
    outfile.write("\n".join(matchData))
    outfile.close()

