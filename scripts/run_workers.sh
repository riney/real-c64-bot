#!/bin/sh

PYTHONPATH=src python src/realc64bot/workers/message_worker.py &
#PYTHONPATH=src python src/realc64bot/gateways/tokenize_worker.py &
#PYTHONPATH=src python src/realc64bot/gateways/reply_worker.py &
