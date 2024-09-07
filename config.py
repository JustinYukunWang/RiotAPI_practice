from typing import Optional, List, Union
from pathlib import Path


requests_header: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
}

BASE_PATH: str = str(Path(__file__).resolve().parent)

DATA_PATH: str = BASE_PATH + "/data"

API_KEY: str = "RGAPI-26e98888-9870-40fa-84a5-ebc311ef1b91"
REGION: str = "americas"
REGION_CODE: str = "na1"
MAX_TIMEOUT: int = 3
API_PROTOCOL = f"https://{REGION}.api.riotgames.com/"
# proper_ID proper_tag
fetch_by_riot_id_api: str = (
    API_PROTOCOL
    + "riot/account/v1/accounts/by-riot-id/{}/{}?api_key="
    + API_KEY
)
# puuid
fetch_by_puuid_api: str = (
    API_PROTOCOL + "riot/account/v1/accounts/by-puuid/{}?api_key=" + API_KEY
)
# match_id
match_details_api = API_PROTOCOL + "lol/match/v5/matches/{}?api_key=" + API_KEY
