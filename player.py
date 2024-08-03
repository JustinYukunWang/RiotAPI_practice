import requests

API_KEY = "RGAPI-08b6a7e8-7744-4d29-bfe6-9a05808625c1"#needs to be updated everytime we log in


#fetch the puuid inorder to fetch the player info later
puuid_fetch_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Voli%20StormValhir/NA1?api_key=RGAPI-08b6a7e8-7744-4d29-bfe6-9a05808625c1"
resp = requests.get(puuid_fetch_url).json()
puuid = resp['puuid']

#fetching player information using puuid
player_info_fetch_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/2IPkTfIvLAU3O9UZzwENXmJOXnyFESoDK6tf4OW9_-dvgqc9AyQflo3MqDQzccDxFN8-focd7JbuLQ?api_key=RGAPI-08b6a7e8-7744-4d29-bfe6-9a05808625c1"
player_info = requests.get(player_info_fetch_url).json()

print(player_info)