ARG PYTHON_VERSION=3.9.7
FROM python:${PYTHON_VERSION}-slim-buster

RUN apt-get update 

RUN apt-get install -y git


COPY . /

ENTRYPOINT ["python3", "/entrypoint.py"]
