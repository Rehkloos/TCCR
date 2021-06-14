import os
import requests
from datetime import datetime
import ujson as json
from dhooks import Webhook, Embed, File
from dotenv import load_dotenv

load_dotenv()
TCI = os.getenv("TWITCH_CLIENT_ID")
TACT = os.getenv("TWITCH_ACCESS_TOKEN")
webhook = os.getenv("CLIPS_WEBHOOK")
file_time = datetime.now().strftime("%Y_%m_%d")

# streamer = "channel name"
STREAMER = "bigbossboze"

URL = f"https://api.twitch.tv/helix/streams?user_login={STREAMER}"
headers = {
    "Client-ID": TCI,
    "Authorization": "Bearer " + TACT,
}


def get_user_id():
    try:
        url = URL
        response = requests.get(url, headers=headers)
        # return
        user_data = response.json()
        user_id = user_data["data"][0]["user_id"]
        return user_id
        # print(user_id)
    except Exception as e:
        print("Unable to retrieve the user ID for " + f"{STREAMER}", e)


def create_clip():
    try:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id=" + get_user_id()
        response = requests.post(url, headers=headers)
        clip_data = response.json()
        clip_link = "https://clips.twitch.tv/" + clip_data["data"][0]["id"]
        hook = Webhook(webhook)
        hook.send(clip_link)

        # create text file that saves clip links and appends links to same file
        txt_file = f"created_clips_{file_time}.txt"
        f = open(txt_file, "a+")
        print(clip_link, file=f)
        f.close()
    except Exception as e:
        print("Couldn't create clip.", e)


def get_clips():
    try:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id=" + get_user_id()
        response = requests.get(url, headers=headers)
        clip_data = response.json()

        saved_json = "clips.json"
        base_path = clip_data["data"]
        api = []
        for each in base_path:
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
    create_clip()
    # get_clips()
