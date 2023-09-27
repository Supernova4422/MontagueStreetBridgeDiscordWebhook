# MontagueStreetBridgeDiscordWebhook
This script will post the latest crash from https://howmanydayssincemontaguestreetbridgehasbeenhit.com/ to a discord webhook. It will also save the date to a text file. The next time it is ran, it will only post if the date is different.

# Where is the unit testing, validation, typing, integration testing, proper naming conventions following PEP, github actions for running static analysis?
I wrote it in 30 minutes, excluding the setting up a docker container, selenium, beautiful soup, all of which are removed now because those broke because Ubuntu deprecated which led to newer python versions deprecating meaning I had to upgrade firefox but those don't work in snap with selenium, which now got all deleted because I learned you can just http get a JS script and it'll return the JSON info of the latest crash and I just retrieved from there instead.

# Are you affiliated with the website, the bridge, Melbourne?
No. I just find it funny.
