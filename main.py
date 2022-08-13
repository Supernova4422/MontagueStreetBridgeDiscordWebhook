import urllib.request
import json
import pathlib
from typing import Optional
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import argparse
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import re
from pyvirtualdisplay import Display

FILENAME = "history.txt"
API_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com/chumps.json"
WEB_URL = "https://howmanydayssincemontaguestreetbridgehasbeenhit.com"

@dataclass
class Entry:
    date: str
    chump_name: str
    chump_url: str
    thanks: str
    thumbnail: str

def run():

    parser = argparse.ArgumentParser(description='Post to a discord webhook.')
    parser.add_argument(
        '--webhook',
        type=str,
        help='Webhook URL for posting to discord')
    args = parser.parse_args()
    discord_url = args.webhook

    current_entry = get_current_entry()
    current_entry = get_current_entry_2()
    current_date = current_entry.date
    last_date = get_last_date()
    if (last_date is not None):
        if current_date == last_date:
            return

    save_date(current_date)
    post(current_entry, discord_url)

def get_current_entry_2() -> str:
    try:
        display = Display(visible=0, size=(1600, 1200))
        display.start()
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        driver.get(WEB_URL)
        contents = driver.page_source
    finally:
        try:
            driver.close()
        finally:
            display.stop()

    soup = BeautifulSoup(contents)

    splitter = "As of "

    found: str = soup.find(text=re.compile('^{}.*'.format(splitter)))
    date = found.split(splitter)[1]
    img = soup.find("img", {"src": "/images/ribbon.png"})
    thumbnail =WEB_URL + img.next_sibling['src']
    chump = img.parent.parent.next_sibling.text
    chump_url = img.parent.parent.next_sibling.find("a")['href']

    entry = Entry(
        date,
        chump,
        chump_url,
        "",
        thumbnail
    )

    return entry

def get_current_entry() -> str:
    contents = urllib.request.urlopen(API_URL).read()
    json_read = json.loads(contents)[0]
    entry = Entry(
        json_read["date_aus_string"],
        json_read["chumps"][0]["name"],
        json_read["chumps"][0]["url"],
        json_read["thanks"],
        WEB_URL + json_read["thumb"]
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
    webhook = DiscordWebhook(
        url=discord_url,
        rate_limit_retry=True,
    )
    embed = DiscordEmbed(
        title=entry.chump_name,
        description=WEB_URL
    )
    embed.set_image(url=entry.thumbnail)

    if entry.thanks != "":
        embed.set_footer(text=entry.thanks)

    embed.add_embed_field(
        name=entry.date,
        value=entry.chump_url
    )

    webhook.add_embed(embed)
    response = webhook.execute()

if __name__ == "__main__":
    run()
