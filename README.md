![image eLasticFM](https://raw.githubusercontent.com/TomasuBE/eLasticFM/main/elasticfm-logo.png)

# eLasticFM
Index all scrobbles into elasticsearch via Last.FM API

# Setup

## Create a mapping for the index template

```
{
  "mappings": {
    "properties": {
      "album": {
        "type": "keyword"
      },
      "artist": {
        "type": "keyword"
      },
      "title": {
        "type": "keyword"
      },
      "user": {
        "type": "keyword"
      }
    }
  }
}
```

Add the index name (ie lastfm) to the index pattern for the template.
Create the index:
```
PUT lastfm
```

## Create a .env file with following parameters

```
LASTFM_USER = 'your-lastfm-username'
LASTFM_API_KEY = 'your-lastfm-apikey'
ELASTIC_ENDPOINT = 'https://your-es-endpoint:9200'
ELASTIC_API_KEY = 'your-elastic-apikey'
```

## Setup Virtual Environment

```
python -m venv venv
source venv/bin/activate
pip3 install -r requirements
#optional: include local CA to certifi bundle, if no cabundle with local CA present)
#cat /usr/local/share/ca-certificates/myCA.crt >> venv/lib/python3.11/site-packages/certifi/cacert.pem
```
Make sure your API Key user has the correct permissions on the  index

## Usage

```
(venv) ~# python3 elasticfm.py
```

or set it as a periodic cron job to regularly update the index.

# Credit

https://www.dataquest.io/blog/last-fm-api-python/


# TODO

- Add genre, image url or image as base64 data
