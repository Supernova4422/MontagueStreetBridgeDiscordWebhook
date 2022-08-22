FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ENV project_path /MontagueStreetBridgeDiscordWebhook
ARG cronjob="*/30 * * * * cd ${project_path} && python3.11 main.py --webhook \$webhook"
RUN echo ${cronjob} 
COPY . ${project_path}
WORKDIR ${project_path}

RUN apt-get -y update
RUN apt install -y software-properties-common cron xvfb curl firefox firefox-geckodriver
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.11 python3.11-distutils python3.11-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.11 get-pip.py
RUN python3.11 -m pip install -r requirements.txt
RUN (crontab -l ; echo "${cronjob}")| crontab -
RUN service cron reload
CMD "cron" "-f"