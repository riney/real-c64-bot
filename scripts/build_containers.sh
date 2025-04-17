#!/bin/sh
docker build -t real-c64-bot/gateways:latest -f docker/Dockerfile.gateways .
docker build -t real-c64-bot/vicetools:latest -f docker/Dockerfile.vicetools .
docker build -t real-c64-bot/worker:latest -f docker/Dockerfile.worker .
