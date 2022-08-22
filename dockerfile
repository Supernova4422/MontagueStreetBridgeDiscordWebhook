FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ENV project_path /MontagueStreetBridgeDiscordWebhook
ARG cronjob="*/30 * * * * cd ${project_path} && python3.9 main.py --webhook"
COPY . ${project_path}
WORKDIR ${project_path}

RUN apt-get -y update
RUN apt install -y software-properties-common cron chromium-chromedriver chromium-browser xvfb curl
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.9 python3.9-distutils python3.9-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
RUN python3.9 -m pip install -r requirements.txt
RUN (crontab -l ; echo "${cronjob} ${webhook}")| crontab -
RUN service cron reload