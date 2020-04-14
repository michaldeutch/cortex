FROM cortex-base:latest

RUN mkdir /usr/src/cortex/server

COPY ./*.py /usr/src/cortex/server/

CMD cd /usr/src/ && python -m cortex.server run-server \
      -h '0.0.0.0'          \
      -p 8000                 \
      'rabbitmq://rabbitmq:5672/'
