from typing import List, Optional, Union
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import (
    REGION,
    REGION_CODE,
    API_KEY,
    fetch_by_riot_id_api,
    fetch_by_puuid_api,
    MAX_TIMEOUT,
    match_details_api,
    requests_header,
)
import requests
import json


def read_csv_data(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, mode="r") as f:
        info = f.read()
    return info.split("\n")


def get_path(*paths: str) -> str:
    return os.path.join(os.path.dirname(__file__), *paths)


def get_match_details(match_id: str) -> dict:
    response = requests.get(
        match_details_api.format(match_id), timeout=MAX_TIMEOUT
    )
    if response.status_code != 200:
        return {}
    response.encoding = response.apparent_encoding
    return json.loads(response.text)


def get_ingame_game_by_puuid(puuid: str) -> dict[str, str]:
    response = requests.get(
        fetch_by_puuid_api.format(puuid),
        timeout=MAX_TIMEOUT,
        headers=requests_header,
    )
    # if response.status_code != 200:
    #     return {}
    response.encoding = response.apparent_encoding
    return json.loads(response.text)
