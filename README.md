[![Build Status](https://travis-ci.org/MicrowavedScrambledEggs/Kaka.svg?branch=mongosearch)](https://travis-ci.org/MicrowavedScrambledEggs/Kaka)

# Let the Kea Fly-integrating genotype storage with KEA

Kaka has three major aims:

- Provide a document based database to store genotype information like GBS results
- The database has to be decentrally distributable
- Continuous integration as well as unit testing techniques shall be used in order to make the deployment safer

## Techniques

Kaka has been developed using 
- Python 2.7 
- The web framework Django 1.8. 
- Travis
- Docker
- PostGreSQL
- Cassandra

## How to run it

Clone github repo from (GitHub)[https://github.com/hdzierz/Kaka]

```
git clone https://github.com/hdzierz/Kaka
cd Kaka
docker-compose up -d
```

You might have to configure Kaka. Please look into (docker-compose.yml)[docker-compose.yml]. Please refer to the (docker compose)[https://docs.docker.com/compose/compose-file/].

## Configure PostGreSQL

Kaka has been configured for running it within the PFR infrastructure. The web servicie will cionnect to it internally so no configuration needed. In case you want to access the DB directly you might have to set the forwarded port to a different value (Change the first value (5434).

Also if not used with PFr you might want to set the proxy servers.

```
db:
  image: postgres
  volumes:
    - .:/dat
  ports:
    - "5434:5432"
  environment:
     - dummy:dummy
     - http_proxy:http://proxy.pfr.co.nz:8080
     - https_proxy:http://proxy.pfr.co.nz:8080
     - no_proxy:localhost,127.0.0.1,*.pfr.co.nz,::1
```

## Configure the web service


If outside PFR you would like to configure the proxy servers, forwarded port (change first number) and the volumes. Don't vchaneg any of the other configurations.

```
web:
  build: .
  dockerfile: Dockerfile_web
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
    - /input:/input
    - /output:/output
    - /workspace:/workspace
  ports:
    - "8000:8000"
  links:
    - db
  environment:
     - dummy:dummy
     - http_proxy:http://proxy.pfr.co.nz:8080
     - https_proxy:http://proxy.pfr.co.nz:8080
     - no_proxy:localhost,127.0.0.1,*.pfr.co.nz,::1
```

