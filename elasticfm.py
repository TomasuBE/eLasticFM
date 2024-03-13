#/usr/bin/python3

# Author:	Thomas Brijs
# Date:		03-12-2024
# eLasticFM Scrobble Indexer

from elasticsearch import Elasticsearch
import datetime as dt
import requests
import certifi
import json
import time

LASTFM_API_KEY = 'your-lastfm-apikey'
LASTFM_USER_AGENT = 'Dataquest'
LASTFM_HITS_PER_PAGE = 200
LASTFM_USER = 'your-lastfm-username'

ELASTIC_HOST = 'https://your-elastic-host:9200'
ELASTIC_API_KEY = 'your-elastic-apikey'

client = Elasticsearch(
  ELASTIC_HOST,
  api_key=ELASTIC_API_KEY
)

#print( client.info() )

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': LASTFM_USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = LASTFM_API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response.json()

responses = []
page = 1
total_pages = 359 # this is just a dummy number so the loop starts

while page <= total_pages:

    payload = {
        'method': 'user.getRecentTracks',
        'user': LASTFM_USER,
        'limit': LASTFM_HITS_PER_PAGE,
        'page': page
    }

    response = lastfm_get(payload)

    print( 'Page: ', page )
    entry = 0
    documents = []
    sources = []
    while entry <= LASTFM_HITS_PER_PAGE - 1:
        timestamp = int(response['recenttracks']['track'][entry]['date']['uts'])
        timestamp = dt.datetime.utcfromtimestamp(timestamp).isoformat()
        artist = response['recenttracks']['track'][entry]['artist']['#text']
        title = response['recenttracks']['track'][entry]['name']
        album = response['recenttracks']['track'][entry]['album']['#text']
        print( timestamp, ' - ', artist, ' - ', title, ' - [', album, ']' )

        source = {
            "artist": artist,
            "title": title,
            "album": album, 
            "@timestamp": timestamp
        }

        client.index(index='search-lastfm', document=source)
        entry += 1
#   TODO: Use bulk create
#   client.bulk(operations=documents, pipeline="ent-search-generic-ingestion")
    time.sleep(3)

    #  update page counts
    page = int(response['recenttracks']['@attr']['page'])
    total_pages = int(response['recenttracks']['@attr']['totalPages'])

    # append response
    responses.append(response)

    page+=1

print(responses)
