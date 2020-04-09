#!/bin/bash

CORTEX_NET="cortex-net"
CORTEX_VOLUME="cortex-volume"
DOCKER_FLAGS="--rm -itd --network=${CORTEX_NET} -v ${CORTEX_VOLUME}:/cortex-storage"

build() {
  echo "=========== Creating Network ============"
  docker network create -d bridge $CORTEX_NET
  echo "=========== Creating Volume ============"
  docker volume create --name $CORTEX_VOLUME
  echo "========= Building cortex-base ========="
  docker build -t cortex-base .
  echo "======== Building cortex-server ========"
  docker build -t cortex-server cortex/server
  echo "======== Building cortex-parser ========"
  docker build -t cortex-parser cortex/parsers
}

run() {
  echo "======== Running rabbitmq ========"
  docker run --rm -d --network=$CORTEX_NET --hostname rabbitmqhost --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
  echo "======== Running mongodb ========"
  docker run --rm -it -d --network=host mongo:latest
  echo "going to sleep.. wait for rabbitmq to stabilize"
  sleep 1m
  echo "========= Running server ========="
  docker run "$DOCKER_FLAGS" cortex-server:latest
  echo "======= Running pose parser ======"
  docker run "$DOCKER_FLAGS" -e "PARSER=pose" cortex-parser:latest
  echo "====== Running color parser ======"
  docker run "$DOCKER_FLAGS" -e "PARSER=color_image" cortex-parser:latest
}

if [ "$1" == 'build' ]; then
  build
else
  if [ "$1" == 'run' ]; then
  run
  else
    build && run
  fi
fi
