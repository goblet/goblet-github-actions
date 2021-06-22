FROM python:3.9.5-alpine3.13

RUN pip install goblet-gcp==0.4.8.1

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
