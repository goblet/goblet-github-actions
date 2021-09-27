FROM python:3.9.5-alpine3.13

RUN pip install goblet-gcp

COPY entrypoint.sh /entrypoint.sh
COPY entrypoint.py /entrypoint.py

# ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT ["python3", "/entrypoint.py"]
