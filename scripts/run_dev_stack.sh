#!/bin/sh
docker compose -f ./docker/docker-compose.yml down
docker compose -f ./docker/docker-compose.yml up
