![eLasticFM Logo](https://raw.githubusercontent.com/TomasuBE/eLasticFM/main/elasticfm-logo.png)

# eLasticFM
Index all scrobbles into elasticsearch via Last.FM API

# Setup

```
python -m venv venv
pip3 install -r requirements
#optional: include local CA to certifi bundle, if no cabundle with local CA present)
cat /usr/local/share/ca-certificates/myCA.crt >> venv/lib/python3.11/site-packages/certifi/cacert.pem
```
Make sure your API Key user has the correct permissions on the  index

# Credit

https://www.dataquest.io/blog/last-fm-api-python/

# TODO

- Create a service that indexes new scrobbles realtime
- Add genre, image url or image as base64 data
