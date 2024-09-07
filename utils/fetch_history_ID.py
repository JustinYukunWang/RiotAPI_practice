import requests
import json
import urllib.parse

API_KEY = "RGAPI-ad33e2ab-8eb1-4bb9-8af6-7cfccabe3d7e"  # needs to be updated everytime we log in
REGION = "americas"


# fetch the puuid inorder to fetch the player info later USING: account: account by riot ID
def get_puuid_using_riotID(gameID, tag):
    proper_ID = urllib.parse.quote(
        gameID
    )  # Change the ID and the tag into url-legal format
    proper_tag = urllib.parse.quote(tag)
    puuid_fetch_url = (
        "https://"
        + REGION
        + ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
        + proper_ID
        + "/"
        + proper_tag
        + "?api_key="
        + API_KEY
    )
    resp = requests.get(puuid_fetch_url).json()
    puuid = resp["puuid"]
    return puuid


# Get recent x amount of match history thru PUUID
def get_match_history(puuid):
    player_matchHistory_fetch_url = (
        "https://"
        + REGION
        + ".api.riotgames.com/lol/match/v5/matches/by-puuid/"
        + puuid
        + "/ids?type=ranked&start=0&count=20&api_key="
        + API_KEY
    )
    matchData = requests.get(player_matchHistory_fetch_url).json()
    return matchData


def get_aThousand_matches(player_puuid, matchData):
    matchData += get_match_history(player_puuid)
    player_list = []
    for match in matchData:
        match_data_fetch_url = (
            "https://"
            + REGION
            + ".api.riotgames.com/lol/match/v5/matches/"
            + match
            + "?api_key="
            + API_KEY
        )
        temp_MatchData = requests.get(match_data_fetch_url).json()
        player_list += temp_MatchData["metadata"][
            "participants"
        ]  # This is a list of PUUIDs of players in that game
    for player in player_list:
        matchData += get_match_history(player)
    return matchData


puuid = get_puuid_using_riotID("Voli StormValhir", "NA1")
print("Running...")
matchData = []
matchData = list(set(get_aThousand_matches(puuid, matchData)))

print(len(matchData))


with open("matchID(Plat-Emerald).txt", "w") as outfile:
    outfile.write("\n".join(matchData))
    outfile.close()
