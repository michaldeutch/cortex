FROM cortex-base:latest

RUN mkdir /usr/src/cortex/server

COPY ./*.py /usr/src/cortex/server/

EXPOSE 8000

CMD cd /usr/src/ && python -m cortex.server run-server \
      -h '127.0.0.1'          \
      -p 8000                 \
      'rabbitmq://127.0.0.1:5672/'
