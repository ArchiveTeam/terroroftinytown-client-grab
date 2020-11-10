FROM python:3-alpine
WORKDIR /grab
COPY . /grab
ENV LC_ALL=C.UTF-8
RUN apk update \
 && apk add --no-cache git \
 && pip install --upgrade seesaw requests
STOPSIGNAL SIGINT
ENTRYPOINT ["run-pipeline3", "--disable-web-server", "pipeline.py"]
