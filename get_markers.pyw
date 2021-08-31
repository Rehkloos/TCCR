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


def get_marker():
    try:
        url = "https://api.twitch.tv/helix/streams/markers?" + twitch.get_user_id()
        r = requests.get(url, headers=headers)
        json_response = r.json()
        marker_data = json_response.get("data", [])
        # hook = Webhook(webhook)
        # hook.send(clip_link)

        saved_json = "markers.json"
        # api = []
        # for each in marker_data:
        #     name = each["id"]
        #     creator_name = each["created_at"]
        #     title = each["title"]
        #     url_path = each["url"]
        #     thumbnail = each["thumbnail_url"]
        #     created_at = each["created_at"]
        #
        #     api.append(
        #         {
        #             "streamer": name,
        #             "title": title,
        #             "thumbnail": thumbnail,
        #             "url_path": url_path,
        #             "creator_name": creator_name,
        #             "created_at": created_at,
        #         }
        #     )

        f = open(saved_json, "w+")
        print(json.dumps(marker_data), file=f)
        f.close()
        # print(api)

    except Exception as e:
        print("Couldn't get markers.", e)


if __name__ == "__main__":
    get_marker()
