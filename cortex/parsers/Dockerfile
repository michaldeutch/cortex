# when running the docker use -e "PARSER=<parser_name>"
# to define the running parsers

FROM cortex-base:latest

RUN mkdir /usr/src/cortex/parsers

COPY ./ /usr/src/cortex/parsers/

CMD cd /usr/src/ &&  python -m cortex.parsers run-parser $PARSER 'rabbitmq://rabbitmq:5672/'
