#!/bin/bash


build() {
  echo "========= Building cortex-base ========="
  docker build -t cortex-base .
  echo "======== Building cortex-server ========"
  docker build -t cortex-server cortex/server
  echo "======== Building cortex-parser ========"
  docker build -t cortex-parser cortex/parsers
}

run() {
  echo "======== Running rabbitmq ========"
  docker run --rm -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
  echo "going to sleep.. wait for rabbitmq to stabilize"
  sleep 1m
  echo "========= Running server ========="
  docker run --rm -d --network=host cortex-server:latest
  echo "======= Running pose parser ======"
  docker run --rm -d --network=host -e "PARSER=pose" cortex-parser:latest
  echo "====== Running color parser ======"
  docker run --rm -d --network=host -e "PARSER=color_image"cortex-parser:latest
}

build
run