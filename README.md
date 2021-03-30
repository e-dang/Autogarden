# Autogarden [![Integrate](https://github.com/e-dang/Autogarden/actions/workflows/integrate.yml/badge.svg?branch=main)](https://github.com/e-dang/Autogarden/actions/workflows/integrate.yml)

## Description
Autogarden is an application for running/managing a microcontroller that can automatically water your plants! Autogarden is designed to allow for indiviual control over each plant that it is watering by controlling a set of valves that restrict water to only the plants that need it. Autogarden is composed of two modules, one written in C++ that runs on the microcontroller, and another written in Python and JavaScript that runs on a server. The server application offers an interface that allows the user to control various settings on the microcontroller, as well as view data that is sent back from the microcontroller.

## Setup
To begin using Autogarden, deploy your own instance of it on a server (if using Heroku see Deploy section for steps). Once the server is running, create a user and a garden instance with your desired configurations. Then, setup a microcontroller with WiFi to control a pump and a set of valves and soil moisture sensors and specify your configuration in the __autogarden.ino__ file found in the __cpp__ directory. Depending on your configuration of pumps, valves, and sensors you may need to write a new autogarden configuration, in which case use the __autogarden.ino__ file as a reference. Additionally, specify the api key, garden name, your wifi ssid and password, and domain name of server in the microcontroller configurations (the api key for the garden, as well as the garden name can be found through the web interface). Then flash the microcontroller with the __*.ino__ file and the microcontroller should now be communicating with the server you setup.

## Deploy

Follow these steps to deploy your own instance of Autogarden to Heroku:
1. Fork repository
2. Add the following to the repositories GitHub Secrets to setup CI
   - EMAIL
   - EMAIL_PASSWORD
   - HEROKU_API_KEY
   - HEROKU_EMAIL
3. Create a Heroku app and specify the heroku app name in __integrate.yml__ in the "Deploy to heroku" step
4. Add nodejs build pack to Heroku app
5. Add Heroku Postgres addon to Heroku app
6. Set Heroku app config vars
   - DJANGO_DEV_MODE_FALSE=False
   - DJANGO_SECRET_KEY
   - EMAIL
   - EMAIL_PASSWORD
   - SITENAME=<span>.herokuapp.com</span>
   - WEB_CONCURRENCY

## Development

Run the following commands:
```
make install && make build
```

Then to  run this application in a development environment create a .env file in the __autogarden__ directory that contains values for the following in the format \<key>=\<value>:
- EMAIL
- EMAIL_PASSWORD

You may also want to follow the steps to setup the GitHub Actions CI environment (see Deploy section) and remove the deploy step in __integrate.yml__.

## Author

- Eric Dang