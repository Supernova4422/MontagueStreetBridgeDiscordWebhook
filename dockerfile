FROM ubuntu

ARG project_path=/MontagueStreetBridgeDiscordWebhook
ARG cronjob="*/30 * * * * cd ${project_path} && python3 main.py --webhook"
ARG webhook="item"

COPY . ${project_path}
WORKDIR ${project_path}

RUN apt-get -y update
RUN apt-get -y install cron chromium-chromedriver chromium-browser xvfb python3 python3-pip
RUN python3 -m pip install -r requirements.txt
RUN (crontab -l ; echo "${cronjob} ${webhook}")| crontab -
RUN service cron reload