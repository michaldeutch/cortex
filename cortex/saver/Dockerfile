FROM cortex-base:latest

RUN mkdir /usr/src/cortex/saver

COPY ./*.py /usr/src/cortex/saver/

CMD cd /usr/src/ && python -m cortex.saver run-saver \
      'mongodb://mongodb:27017/'   \
      'rabbitmq://rabbitmq:5672/'
