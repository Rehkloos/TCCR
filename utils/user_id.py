import os

import requests
from dotenv import load_dotenv

load_dotenv()
TCI = os.getenv("TWITCH_CLIENT_ID")
TACT = os.getenv("TWITCH_ACCESS_TOKEN")

params = {"user_login": "iitztimmy"}

URL = "https://api.twitch.tv/helix/streams?"
headers = {
    "Client-ID": TCI,
    "Authorization": "Bearer " + TACT,
}


class twitch_utils:
    def get_user_id(self):
        try:
            url = URL
            response = requests.get(url, params=params, headers=headers)
            # return
            user_data = response.json()
            user_id = user_data["data"][0]["user_id"]
            return user_id
            print(user_id)
        except Exception as e:
            print("Unable to retrieve the user ID for " + f"{params}", e)
