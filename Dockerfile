FROM python:3.12-slim
COPY entrypoint.sh /opt/app/entrypoint.sh
COPY app.py /opt/app/app.py
ENTRYPOINT ["/opt/app/entrypoint.sh"]
