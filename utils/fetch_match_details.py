from utils import (
    read_csv_data,
    get_path,
    get_match_details,
    get_ingame_game_by_puuid,
)
from config import DATA_PATH
from tqdm import tqdm

match_ids = read_csv_data(get_path(DATA_PATH, "NA_MatchIDs.csv"))[1:]


for id in tqdm(match_ids[:50]):
    match_details = get_match_details(id)
    if match_details:

        with open(
            get_path(DATA_PATH, "matches", f"{id}.csv"),
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(
                "player_name, player_tagline, player_champion_name, player_items, player_kills, player_death, player_assists, player_level, player_position, player_experience, player_gold_earned, player_cs, player_cs_jg\n"
            )

        for player in match_details["info"]["participants"]:
            player_name_info = get_ingame_game_by_puuid(player["puuid"])
            player_game_name = player_name_info.get("gameName")
            player_tag_line = player_name_info.get("tagLine")
            player_champion_name = player["championName"]
            player_items = [player[f"item{i}"] for i in range(7)]
            player_kills = player["kills"]
            player_death = player["deaths"]
            player_assists = player["assists"]
            player_level = player["champLevel"]
            player_position = player["individualPosition"]
            player_experience = player["champExperience"]
            player_gold_earned = player["goldEarned"]
            player_cs_jg = player["neutralMinionsKilled"]
            player_cs = player["totalMinionsKilled"]

            with open(
                get_path(DATA_PATH, "matches", f"{id}.csv"),
                mode="a+",
                encoding="utf-8",
            ) as f:
                f.write(
                    f"{player_game_name}, {player_tag_line}, {player_champion_name}, {player_items}, {player_kills}, {player_death}, {player_assists}, {player_level}, {player_position}, {player_experience}, {player_gold_earned}, {player_cs}, {player_cs_jg}\n"
                )
        print(f"{id} - Finish.")
