FROM python:3.4-alpine
ARG repo=https://github.com/ArchiveTeam/terroroftinytown-client-grab
ARG branch=master
ENV LC_ALL=C.UTF-8
RUN apk update \
 && apk add --no-cache git \
 && pip install --upgrade seesaw requests \
 && git clone "${repo}" grab \
 && cd grab \
 && git checkout "${branch}"
WORKDIR /grab
STOPSIGNAL SIGINT
ENTRYPOINT ["run-pipeline3", "--disable-web-server", "pipeline.py", "--concurrent", "2", "YOURNICKHERE"]
