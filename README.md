# WRLC Legacy Catalog Redirect Service
Simple service that takes legacy bibid's and tries to find migrated records in Primo. This service works by looking up a legacy bibid in an elasticsearch index of old records, and then trying to construct a search that will yeild the new Alma/Primo record for the same item.

## Installation
Clone this repository.
```
git clone git@github.com:WRLC/catalog-redirects.git
```

Set up python virtual environment
```
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Configure your application service. At WRLC we now run this app in a [Green Unicorn](https://docs.gunicorn.org/en/stable/index.html) Python WSGI HTTP server). The daemon is started and stoped via systemd.

```
mkdir log
sudo cp catalog-redirects.service.example /etc/systemd/system/catalog-redirects.service
sudo vim /etc/systemd/system/catalog-redirects.service
sudo systemctl start catalog-redirects.service
sudo systemctl enable catalog-redirects.service
```

## To be done
Add a settings file so the Elastic Search index endpoint can be configurable.

## Deprecated Docker configuration
All hard-coded in Dockerfile:
```
docker pull wrlc/catalog-redirects
docker run -d -p 5000:5000 wrlc/catalog-redirects
```
With docker compose:
create a docker-compose.yml file that looks like this:
```
version: "3"
services:
  catalog-redirects:
    image: wrlc/catalog-redirects
    ports:
      - 5000:5000
    restart: always
```
Run your service:
```
docker-compose up -d
```
