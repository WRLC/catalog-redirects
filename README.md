# WRLC Legacy Catalog Redirect Service
Prototype application that takes legacy bibid's and tries to find migrated records in Primo. This service works by looking up a legacy bibid in an elasticsearch index of old records, and then trying to construct a search taht will yeild the new Alma/Primo record for the same item.

## configuration
All hard-coded for now.
```
docker pull wrlc/catalog-redirects
docker run -d -p 5000:5000 wrlc/catalog-redirects
```
### With docker compose:
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
