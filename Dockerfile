# A base docker for all other dockers to use FROM
# Downloads projects requirements and copies utils - for each package to use

FROM ubuntu:latest

COPY requirements.txt /usr/src/requirements.txt

RUN mkdir /usr/src/cortex
COPY cortex/__init__.py /usr/src/cortex/__init__.py

RUN mkdir /usr/src/cortex/utils
COPY cortex/utils /usr/src/cortex/utils/


RUN apt-get update \
  && apt-get install -y python3.8 python3-pip\
  && python3.8 -m pip install --upgrade pip setuptools wheel \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3.8 python \
  && python3.8 -m pip install --upgrade pip setuptools wheel

RUN pip install -r /usr/src/requirements.txt