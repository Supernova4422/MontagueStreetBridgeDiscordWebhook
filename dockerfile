FROM ubuntu:18.04

ENV project_path /MontagueStreetBridgeDiscordWebhook
ARG cronjob="*/30 * * * * cd ${project_path} && python3 main.py --webhook"

COPY . ${project_path}
WORKDIR ${project_path}

RUN apt-get -y update
RUN apt install -y software-properties-common cron chromium-chromedriver chromium-browser xvfb
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.9 python3.9-distutils
RUN python3.9 -m pip install -r requirements.txt
RUN (crontab -l ; echo "${cronjob} ${webhook}")| crontab -
RUN service cron reload