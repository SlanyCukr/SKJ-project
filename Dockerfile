FROM python:3.8-slim-buster

WORKDIR /skj-project

RUN apt-get update && apt-get install -y curl wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-u", "-m", "scraper.scraper_novinky"]