import os
from datetime import datetime

import requests
import ujson as json
from dotenv import load_dotenv
from utils.user_id import twitch_utils

twitch = twitch_utils()

load_dotenv()
TCI = os.getenv("TWITCH_CLIENT_ID")
TACT = os.getenv("TWITCH_ACCESS_TOKEN")
webhook = os.getenv("CLIPS_WEBHOOK")
streamer_name = os.getenv("STREAMER")
file_time = datetime.now().strftime("%Y_%m_%d")

headers = {
    "Client-ID": TCI,
    "Authorization": "Bearer " + TACT,
}


def get_clips():
    try:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id=" + twitch.get_user_id()
        r = requests.get(url, headers=headers)
        json_response = r.json()
        clip_data = json_response.get("data", [])

        saved_json = "clips.json"
        api = []
        for each in clip_data:
            name = each["broadcaster_name"]
            creator_name = each["creator_name"]
            title = each["title"]
            url_path = each["url"]
            thumbnail = each["thumbnail_url"]
            created_at = each["created_at"]

            api.append(
                {
                    "streamer": name,
                    "title": title,
                    "thumbnail": thumbnail,
                    "url_path": url_path,
                    "creator_name": creator_name,
                    "created_at": created_at,
                }
            )

        f = open(saved_json, "w+")
        print(json.dumps(api), file=f)
        f.close()
        print(api)
        # return clip_data
    except Exception as e:
        print("Couldn't create clip.", e)


if __name__ == "__main__":
    get_clips()
