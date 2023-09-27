FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV project_path /MontagueStreetBridgeDiscordWebhook
COPY . ${project_path}
WORKDIR ${project_path}

RUN apt-get -y update
RUN apt install -y python3 python3-pip
RUN python3 -m pip install -r requirements.txt

CMD "python3" "${project_path}/main.py" "--webhook" "$webhook"
