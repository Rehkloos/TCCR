import os
from datetime import datetime

import requests
from dhooks import Webhook
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


def create_clip():
    try:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id=" + twitch.get_user_id()
        r = requests.post(url, headers=headers)
        json_response = r.json()
        clip_data = json_response.get("data", [])
        clip_link = "https://clips.twitch.tv/" + clip_data[0]["id"]
        hook = Webhook(webhook)
        hook.send(clip_link)

        # create text file that saves clip links and appends links to same file
        txt_file = f"created_clips_{file_time}.txt"
        f = open(txt_file, "a+")
        print(clip_link, file=f)
        f.close()
    except Exception as e:
        print("Couldn't create clip.", e)


if __name__ == "__main__":
    create_clip()
