#!/bin/bash
screen -S scraper -dm python3 -m scraper.scraper_novinky
screen -S graphql_server -dm python3 -m graphql_backend.server
screen -S ngrok -dm ./ngrok http -region eu 3000

cd frontend
screen -S react -dm npm start