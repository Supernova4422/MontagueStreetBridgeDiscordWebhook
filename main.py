import urllib.request
import argparse
import requests
import pathlib
import re
import json
from time import sleep
from typing import Optional

FILENAME = "history.txt"
API_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com/chumps.json"
WEB_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com"

class Entry:
    def __init__(self, date: str, chump_name: str, chump_url: str, thanks: str, thumbnail: str):
        self.date = date
        self.chump_name = chump_name
        self.chump_url = chump_url
        self.thanks = thanks
        self.thumbnail = thumbnail

    def to_json(self) -> str:
        embed = {
            "title": self.chump_name,
            "description": WEB_URL,
            "fields": [
                { 
                    "name": self.date,
                    "value": self.chump_url
                },
            ],
            "image": {
                "url": self.thumbnail
            }
        }

        # entry.thanks is unsused!!!

        result = {
            "embeds" : [
                embed
            ]
        }
        
        return result


def run():
    print("Starting")
    parser = argparse.ArgumentParser(description='Post to a discord webhook.')
    parser.add_argument(
        '--webhook',
        type=str,
        help='Webhook URL for posting to discord')
    args = parser.parse_args()
    discord_url = args.webhook
    current_entry = get_current_entry()
    current_date = current_entry.date
    last_date = get_last_date()
    if (last_date is not None):
        if current_date == last_date:
            print("No new crash found.")
            return

    print("New crash found")
    post(current_entry, discord_url)
    save_date(current_date)

def get_current_entry() -> str:
    print("fetching")
    request = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    urlopen = urllib.request.urlopen(request)
    readContents = urlopen.read()
    contents = readContents.decode("utf-8")

    json_entry = json.loads(contents)[0]

    entry = Entry(
        json_entry["date"],
        json_entry["name"],
        json_entry["url"] if "url" in json_entry else "",
        json_entry["thanks"] if "thanks" in json_entry else "",
        (WEB_URL + json_entry.get("image", "")) if "image" in json_entry else ""
    )

    return entry

def get_last_date() -> Optional[str]:
    """Get the last date saved."""
    if not pathlib.Path(FILENAME).exists():
        return None

    with open(FILENAME, 'r') as f:
        return f.read()

def save_date(date: str):
    """Saves the date of the last crash."""
    with open(FILENAME, 'w') as f:
        f.write(date)

def post(entry: Entry, discord_url: str):
    print(discord_url)
    data = entry.to_json()
    result = requests.post(discord_url, json = data)
    result.raise_for_status()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(e)
    finally:
        print("sleeping")
        sleep(20 * 60)
