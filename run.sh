#!/bin/bash
screen -S scraper -dmL python3 -m scraper.scraper_novinky
screen -S graphql_server -dm python3 -m graphql_backend.server
screen -S alert_server -dm python3 -m alert_system.server
cd frontend
screen -S react -dm npm start
