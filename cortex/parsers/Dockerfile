# when running the docker use -e "PARSER=<parser_name>"
# to define the running parser

FROM cortex-base:latest

RUN mkdir /usr/src/cortex/parsers

COPY ./ /usr/src/cortex/parsers/

CMD cd /usr/src/ &&  python -m cortex.parsers run-parser $PARSER 'rabbitmq://127.0.0.1:5672/'
