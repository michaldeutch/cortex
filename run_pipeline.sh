#!/bin/bash

RABBIT='rabbitmq://127.0.0.1:5672'
MONGO='mongodb://mongodb:27017/'

run() {
  echo "======== Running rabbitmq ========"
  docker run --rm -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
  echo "======== Running mongodb ========"
  docker run --rm -d -p 27017:27017 mongo:latest
  echo "going to sleep.. wait for rabbitmq to stabilize"
  sleep 1m
  python -m cortex.server run-server $RABBIT &>/dev/null &
  server=$!
  python -m cortex.parsers run-parser 'pose' $RABBIT &>/dev/null &
  pose=$!
  python -m cortex.parsers run-parser 'feelings' $RABBIT &>/dev/null &
  feelings=$!
  python -m cortex.parsers run-parser 'color_image' $RABBIT &>/dev/null &
  color=$!
  python -m cortex.parsers run-parser 'depth_image' $RABBIT &>/dev/null &
  depth=$!
  python -m cortex.saver run-saver $MONGO $RABBIT &>/dev/null &
  saver=$!
  python -m cortex.api run-server &>/dev/null &
  api=$!
  python -m cortex.gui run-server &>/dev/null &
  gui=$!

  echo "Ran all cortex, hit ctrl+c to kill them all"
  echo "Wait a few more seconds for my GUI to open in your browser!"
  wait
}

finish() {
  echo ""
  echo "killing :("
  kill $server $pose $feelings $color $depth $saver $api $gui
}

trap 'finish' SIGINT

run
