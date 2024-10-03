FROM python:3.12-slim
RUN apt-get update && apt-get install -y  openjdk-17-jdk software-properties-common wget
COPY requirements.txt /opt/app/requirements.txt
RUN pip3 install -r /opt/app/requirements.txt
COPY src /opt/app/src
COPY entrypoint.sh /opt/app/entrypoint.sh
COPY app.py /opt/app/app.py
RUN wget https://ostrovok.tech/hackathon/data/track_2/rates_clean.csv -O /opt/app/rates_clean.csv
ENTRYPOINT ["/opt/app/entrypoint.sh"]
