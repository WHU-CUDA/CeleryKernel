FROM nvidia/cuda:11.4.1-base-ubuntu18.04

MAINTAINER "wangx"

ADD . /app
WORKDIR /app

RUN apt-get update \
  && apt-get install -y python3-pip python3.6 \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && export LC_ALL=C.UTF-8 \
  && export LANG=C.UTF-8 \
  && cd /app \
  && pip install -r  requirements.txt \
  && chmod a+x run.sh


