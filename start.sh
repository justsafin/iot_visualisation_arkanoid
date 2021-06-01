#!/bin/bash

sudo apt-get install docker docker-compose
sudo docker-compose up -d
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install paho-mqtt
pip3 install numpy
pip3 install influxdb
pip3 install pandas
pip3 install seaborn
pip3 install matplotlib
python3 ./main.py
