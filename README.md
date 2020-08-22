[![Build Status](https://travis-ci.com/lilasaba/library_backend.svg?branch=master)](https://travis-ci.com/lilasaba/library_backend)

# Book Library Backend

Containerized Flask API's served by PostgreSQL.

### Build and launch db and application

```
docker-compose build db
docker-compose build test-postgresql
docker-compose run test-postgresql
docker-compose build test
docker-compose run test
docker-compose build static-analysis
docker-compose run static-analysis
docker-compose build server
docker-compose run -p 127.0.0.1:8000:8000/tcp server
```


### Call API.

```
cd library_backend
python call_api.py
```
