#!/bin/sh
docker image build -f docker/Dockerfile.vicetools -t realc64bot/vicetools .
docker image build -f docker/Dockerfile.test -t realc64bot/test .
