#!/bin/bash

CORTEX_NET="cortex-net"
CORTEX_VOLUME="cortex-volume"
DOCKER_FLAGS="--rm -d --network=${CORTEX_NET} -v ${CORTEX_VOLUME}:/cortex-storage"

build() {
  echo "=========== Creating Network ============"
  docker network create -d bridge $CORTEX_NET
  echo "=========== Creating Volume ============"
  docker volume create --name $CORTEX_VOLUME
  echo "========= Building cortex-base ========="
  docker build -t cortex-base .
  echo "======== Building cortex-server ========"
  docker build -t cortex-server cortex/server
  echo "========= Building cortex-pose ========="
  docker build -t cortex-pose cortex/parsers
  echo "======= Building cortex-feelings ======="
  docker build -t cortex-feelings cortex/parsers
  echo "======== Building cortex-color ========="
  docker build -t cortex-color cortex/parsers
  echo "======== Building cortex-depth ========="
  docker build -t cortex-depth cortex/parsers
  echo "======== Building cortex-saver ========="
  docker build -t cortex-saver cortex/saver
  echo "========= Building cortex-api =========="
  docker build -t cortex-api cortex/api
}

run() {
  echo "======== Running rabbitmq ========"
  docker run --rm -d --network=$CORTEX_NET --hostname rabbitmqhost --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
  echo "======== Running mongodb ========"
  docker run --rm -d --network=$CORTEX_NET --hostname mongodbhost --name mongodb -p 27017:27017 mongo:latest
  echo "going to sleep.. wait for rabbitmq to stabilize"
  sleep 1m
  echo "========= Running server ========="
  docker run $DOCKER_FLAGS -p 8000:8000 cortex-server:latest
  echo "======= Running pose parser ======"
  docker run $DOCKER_FLAGS -e "PARSER=pose" cortex-pose:latest
  echo "==== Running feelings parser ====="
  docker run $DOCKER_FLAGS -e "PARSER=color_feelings" cortex-feelings:latest
  echo "====== Running color parser ======"
  docker run $DOCKER_FLAGS -e "PARSER=color_image" cortex-color:latest
  echo "====== Running depth parser ======"
  docker run $DOCKER_FLAGS -e "PARSER=depth_image" cortex-depth:latest
  echo "========= Running saver =========="
  docker run $DOCKER_FLAGS cortex-saver:latest
  echo "========== Running api ==========="
  docker run $DOCKER_FLAGS -p 5000:5000 cortex-api:latest
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
