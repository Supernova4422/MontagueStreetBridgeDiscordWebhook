import urllib.request
import json
import pathlib
from typing import Optional
from discord_webhook import DiscordWebhook, DiscordEmbed
import argparse

FILENAME = "history.txt"
API_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com/chumps.json"
WEB_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com"

def run():

    parser = argparse.ArgumentParser(description='Post to a discord webhook.')
    parser.add_argument(
        '--webhook',
        type=str,
        help='Webhook URL for posting to discord')
    args = parser.parse_args()
    discord_url = args.webhook

    current_entry = get_current_entry()
    current_date = current_entry['date']
    last_date = get_last_date()
    if (last_date is not None):
        if current_date == last_date:
            return

    save_date(current_date)
    post(current_entry, discord_url)

def get_current_entry() -> str:
    contents = urllib.request.urlopen(API_URL).read()
    json_read = json.loads(contents)
    return json_read[0]

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

def post(entry, discord_url: str):
    webhook = DiscordWebhook(
        url=discord_url,
        rate_limit_retry=True,
    )
    embed = DiscordEmbed(
        title=entry["chumps"][0]["name"],
        description=WEB_URL
    )
    embed.set_image(url= WEB_URL + entry["thumb"])
    embed.set_footer(text=entry["thanks"])
    embed.add_embed_field(
        name=entry["date_aus_string"],
        value=entry["chumps"][0]["url"]
    )

    webhook.add_embed(embed)
    response = webhook.execute()

if __name__ == "__main__":
    run()
