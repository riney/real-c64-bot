import json
import logging
import time

import requests
from redis import Redis
from rq import Queue
from TwitterAPI import (TwitterAPI, TwitterConnectionError, TwitterOAuth, TwitterRequestError)

from realc64bot.workers import execute_tweet

CONFIG_FILE = 'config.json'
QUERY = 'to:realc64bot'
DEBUG_REQUESTS = False

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

# TWITTER API METHODS
def get_rules(api):
    res = api.request('tweets/search/stream/rules', method_override='GET')

    if res.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(res.status_code, res.text)
        )
    return res.json()

def delete_all_rules(api):
	rules = get_rules(api)

	if rules is None or "data" not in rules:
		return None

	ids = list(map(lambda rule: rule["id"], rules["data"]))
	res = api.request('tweets/search/stream/rules', { "delete": { "ids": ids } })

	if res.status_code != 200:
		raise Exception(
			"Cannot delete rules (HTTP {}): {}".format(res.status_code, res.text)
		)

def set_rules(api, rules):
	res = api.request('tweets/search/stream/rules', { 'add': rules })
	if res.status_code != 201: exit()

	if res.status_code != 201:
		raise Exception(
			"Cannot add rules (HTTP {}): {}".format(res.status_code, res.text)
		)

def enable_requests_debugging():
	if DEBUG_REQUESTS:
		print("Enabling requests debugging.")

		try:
			import http.client as http_client
		except ImportError:
			# Python 2
			import httplib as http_client
		http_client.HTTPConnection.debuglevel = 1

		# You must initialize logging, otherwise you'll not see debug output.
		logging.basicConfig()
		logging.getLogger().setLevel(logging.DEBUG)
		requests_log = logging.getLogger("requests.packages.urllib3")
		requests_log.setLevel(logging.DEBUG)
		requests_log.propagate = True

# REDIS METHODS
def handle_tweet(tweet):
	print("Enqueueing tweet")
	q.enqueue(execute_tweet, tweet) 

def main():
	try:
		enable_requests_debugging()
		load_configuration()
		connect_to_redis()

		o = TwitterOAuth.read_file('./credentials.txt')
		api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

		# ADD STREAM RULES
		print("Configuring stream rules.")
		delete_all_rules(api)
		set_rules(api, [{ 'value': QUERY }])
		get_rules(api)

		# START STREAM
		print("Starting.")
		while True:
			try:
				stream = api.request('tweets/search/stream')
				if stream.status_code != 200: 
					print(f"Loop start received status code {stream.status_code}, exiting")
					exit()
				for item in stream:
					print(f"Received item: {item}")
					if 'data' in item:
						handle_tweet(item['data'])
					elif 'disconnect' in item:
						event = item['disconnect']
						print('Received disconnect')
						if event['code'] in [2,5,6,7]:
							# something needs to be fixed before re-connecting
							print(f"Event code is {event['code']}")
							raise Exception(event['reason'])
						else:
							print('Other problem; re-trying')
							stream = None
							time.sleep(5)
							break
			except TwitterRequestError as e:
				if e.status_code < 500:
					# something needs to be fixed before re-connecting
					print("Real bad problem; falling out")
					raise
				else:
					# temporary interruption, re-try request
					print('Twitter request error, re-trying.')
					stream = None
					time.sleep(5)
					pass
			except TwitterConnectionError as tce:
				# temporary interruption, re-try request
				print(f"Twitter connection error, re-trying.")
				print(tce)

				stream = None
				time.sleep(5)
				pass


	except TwitterRequestError as e:
		print('Top-level TwitterRequestError caught.')
		print(e.status_code)
		for msg in iter(e):
			print(msg)

	except TwitterConnectionError as e:
		print('Top-level TwitterConnectionError caught.')
		print(e)

	except Exception as e:
		print('Top-level Exception caught.')
		print(e)

if __name__ == "__main__":
	main()