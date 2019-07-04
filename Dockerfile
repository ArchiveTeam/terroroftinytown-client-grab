FROM python:3.4
ARG repo=https://github.com/ArchiveTeam/terroroftinytown-client-grab
ARG branch=master
ENV LC_ALL=C.UTF-8
RUN apt update \
 && apt install -y --no-install-recommends git-core \
 && pip install --upgrade seesaw requests \
 && git clone "${repo}" grab \
 && cd grab \
 && git checkout "${branch}"
WORKDIR /grab
STOPSIGNAL SIGINT
ENTRYPOINT ["run-pipeline3", "--disable-web-server", "pipeline.py", "--concurrent", "2", "YOURNICKHERE"]
