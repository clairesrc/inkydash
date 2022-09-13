#!/bin/sh
docker-compose down
docker build -t inkydash . && docker-compose up -d inkydash
sleep 1
curl http://localhost:8080/data | jq .[0].data

