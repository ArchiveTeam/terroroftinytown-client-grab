FROM python:3.8-alpine
WORKDIR /grab
COPY . /grab

ENV LC_ALL=C.UTF-8
STOPSIGNAL SIGINT
ENTRYPOINT ["run-pipeline3", "--disable-web-server", "pipeline.py"]
