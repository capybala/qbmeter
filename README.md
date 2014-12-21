QB Meter
=======

Scrapy spider to show stats of QB House's availability.

Requirements
------------

* Python 2.7
* Virtualenv

Usage
-----

### Setup local development environment

```
git clone https://github.com/orangain/qbmeter
cd qbmeter
virtialenv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Setup Cloudant database

1. Create Cloudant database e.g. `qbmeter`.
2. Generate API key for the database.
3. Grant write access on the database to the API user, and read access to Everyone.
4. Put `.env` file.

```
# e.g. CLOUDANT_URL=https://orangain.cloudant.com/qbmeter
CLOUDANT_URL=YOUR_CLOUDANT_DB_URL
CLOUDANT_USER=YOUR_API_KEY
CLOUDANT_PASSWORD=YOUR_API_PASSWORD
```

### Run spider

```
./scripts/run_spider.sh
```

### Insert data into Cloudant

```
./scripts/update_data.sh
```
