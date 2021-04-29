#!/bin/bash
pip3 install -r requirements.txt

chmod +x run.sh
chmod +x stop.sh

sudo apt-get install nodejs npm

cd frontend
npm install
