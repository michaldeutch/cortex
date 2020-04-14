FROM cortex-base:latest

RUN mkdir /usr/src/cortex/api

COPY ./*.py /usr/src/cortex/api/

CMD cd /usr/src/ && python -m cortex.api run-server \
      -h 0.0.0.0 \
      -d 'mongodb://mongodb:27017/'   \