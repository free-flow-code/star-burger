#!/usr/bin/env bash
set -e
cd /opt/star-burger
git fetch
git pull star-burger master
echo -e "\e[1;32m Files updated.\e[0m"
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml reload nginx
echo -e "\e[1;32m Deploy completed!\e[0m"
