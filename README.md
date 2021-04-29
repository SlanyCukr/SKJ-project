# Novinky.cz scraper
## Installation
1. Make installation script executable `chmod +x install.sh`
2. Run the installation script `./install.sh`
3. Handle the chromium browser driver installation

## Run the scraper
The scraper has command-line interface.

`python3 run.py` or
`python3 run.py --help`

## Stop the scraper
`./stop.sh`

## Raspberry PI LED, sound client
### Install dependencies
`pip3 install -r alert_system/requirements.txt`

### Run the client
1. `screen -S "scraper_client"`
2. `sudo python3 -m alert_system.client`

### Frontend GraphQL server settings
You need to manually point React page to GraphQL server, if you are trying to use remote instance of GraphQL server, or if you changed GraphQL server port. This can be done in the Settings section in React page (image below).

### Live instance
Dashboard is up and running at [http://31.31.74.93:3000/](http://31.31.74.93:3000/)
