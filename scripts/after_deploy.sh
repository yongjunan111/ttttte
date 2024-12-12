#!/bin/bash
REPOSITORY=/home/ubuntu/

cd $REPOSITORY/real_last_test

echo "> 🔵 Stop & Remove docker services."
sudo docker-compose down

echo "> 🟢 Run new docker services."
sudo docker-compose up -d --build >> /var/log/deploy.log 2>&1
