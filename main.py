import json
import logging
import time
import requests
from redis import Redis
from rq import Queue

from realc64bot.workers import execute_tweet

CONFIG_FILE = 'config.json'

config = None
redis = None
q = None

# CONFIGURATION METHODS
def load_configuration():
	global config
	try:
		print(f"Loading configuration from {CONFIG_FILE}")
		with open(CONFIG_FILE) as f:
			config = json.load(f)
			
	except JSONDecodeError as e:
		print(e)

# REDIS METHODS
def connect_to_redis():
	global redis, q
	print(f"Connecting to job queue at {config['redis']['host']}")
	redis = Redis(host=config['redis']['host'], port=config['redis']['port'])
	q = Queue(connection=redis)

def main():
	try:
		load_configuration()
		connect_to_redis()

if __name__ == "__main__":
	main()