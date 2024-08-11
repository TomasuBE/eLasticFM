from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import datetime as dt
import requests
import certifi
import json
import time
import os
import logging

load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
LASTFM_USER_AGENT = 'Dataquest'
LASTFM_HITS_PER_PAGE = 200
LASTFM_USERNAME = os.getenv('LASTFM_USER')

ELASTIC_HOST = os.getenv('ELASTIC_ENDPOINT')
ELASTIC_API_KEY = os.getenv('ELASTIC_API_KEY')

logging.basicConfig(level=logging.INFO)

first_time = False

client = Elasticsearch(
  ELASTIC_HOST,
  api_key=ELASTIC_API_KEY
)

logging.debug( client.info() )
try:
    resp = client.search(index="lastfm", query={"match_all": {}}, size=1, sort="@timestamp:desc")
    last_scrobble = dt.datetime.fromisoformat(resp['hits']['hits'][0]['_source']['@timestamp'])
    logging.debug( last_scrobble )
except:
    first_time = True

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': LASTFM_USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = LASTFM_API_KEY
    payload['format'] = 'json'

    logging.debug('Payload: ', payload)

    response = requests.get(url, headers=headers, params=payload)
    return response.json()

responses = []
page = 1
total_pages = 359 # this is just a dummy number so the loop starts

while page <= total_pages:

    payload = {
        'method': 'user.getRecentTracks',
        'user': LASTFM_USERNAME,
        'limit': LASTFM_HITS_PER_PAGE,
        'page': page
    }

    response = lastfm_get(payload)
    logging.debug('Response: ', json.dumps(response))
    entry = 0
    documents = []
    sources = []
    if 'date' not in response['recenttracks']['track'][entry]:
        #skip current playing since it has no timestamp yet
        entry += 1
    while entry < LASTFM_HITS_PER_PAGE:
        timestamp = int(response['recenttracks']['track'][entry]['date']['uts'])
        timestamp = dt.datetime.utcfromtimestamp(timestamp)
        if not first_time:
            logging.debug( 'Updating' )
            if timestamp <= last_scrobble:
                logging.info('Up to date.')
                break

        timestamp = timestamp.isoformat()
        artist = response['recenttracks']['track'][entry]['artist']['#text']
        title = response['recenttracks']['track'][entry]['name']
        album = response['recenttracks']['track'][entry]['album']['#text']
        print( timestamp, ' - ', artist, ' - ', title, ' - [', album, ']' )

        source = {
            "artist": artist,
            "title": title,
            "album": album,
            "user": LASTFM_USERNAME,
            "@timestamp": timestamp
        }

        client.index(index='lastfm', document=source)

        entry += 1

    # TODO: Use bulk update to insert multiple docs in 1 call
    #client.bulk(operations=json.loads(json.dumps(doc)), index="search-lastfm")
    if not first_time:
        if timestamp <= last_scrobble:
            logging.info('Exiting')
            break

    time.sleep(3)
    # extract pagination info
    page = int(response['recenttracks']['@attr']['page'])
    total_pages = int(response['recenttracks']['@attr']['totalPages'])

    # append response
    responses.append(response)

    page+=1

logging.info('Finished')
