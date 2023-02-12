#!/bin/sh
docker build -f docker/Dockerfile.vicetools -t realc64bot/vicetools .
docker build -f docker/Dockerfile.test -t realc64bot/test .
