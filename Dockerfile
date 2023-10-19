ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim-buster

RUN apt-get update 

RUN apt-get install -y git


COPY entrypoint.py /entrypoint.py
COPY . /

ENTRYPOINT ["python3", "/entrypoint.py"]
