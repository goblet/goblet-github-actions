FROM python:3.11.4-slim-buster

RUN apt-get update

RUN apt-get install -y git

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python3", "/entrypoint.py"]
