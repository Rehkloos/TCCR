import os
from datetime import datetime

import requests
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
    "Content-Type": "application/json",
}
data = {"user_id": twitch.get_user_id(), "description": "hello, this is a marker!"}


def create_marker():
    try:
        url = "https://api.twitch.tv/helix/streams/markers"
        r = requests.post(url, headers=headers, data=data)
        json_response = r.json()
        marker_data = json_response.get("data", [])
        marker_id = marker_data[0]["id"]
        marker_created = marker_data[0]["created_at"]
        # hook = Webhook(webhook)
        # hook.send(clip_link)

        # create text file that saves clip links and appends links to same file
        txt_file = f"created_markers_{file_time}.txt"
        f = open(txt_file, "a+")
        print(marker_id, file=f)
        print(marker_created, file=f)
        f.close()
    except Exception as e:
        print("Couldn't create marker.", e)


if __name__ == "__main__":
    create_marker()
