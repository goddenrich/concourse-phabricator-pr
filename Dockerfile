FROM alpine:latest AS resource

RUN apt-get install git php5-cli php-curl
RUN git clone https://secure.phabricator.com/source/libphutil.git
RUN git clone https://secure.phabricator.com/diffusion/ARC/arcanist.git
COPY arcanist/bin/arc /usr/local/bin/

RUN git config --global user.email "git@localhost"
RUN git config --global user.name "git"

ADD assets/ /opt/resource/
RUN chmod +x /opt/resource/*

FROM resource AS tests
ADD test/ /tests
RUN /tests/all.sh

FROM resource
