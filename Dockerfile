FROM alpine:latest as resource

RUN set -ex; \
  apk add --update \
  ca-certificates \
  curl \
  git \
  jq \
  openssh-client \
  ; \
  rm -rf /var/cache/apk/*;

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN pip install phabricator

RUN git config --global user.email "git@localhost"
RUN git config --global user.name "git"

ADD assets/ /opt/resource/
RUN chmod +x /opt/resource/*

RUN echo '{"source": {"uri":"https://c4science.ch/", "token": "cli-uu36lofw44npy374a3wgfbi3num7"}, "version": {"diff": 907}}' | python3 /opt/resource/commands/check.py | jq
