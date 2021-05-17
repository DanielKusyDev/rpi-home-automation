# rpi-home-automation

This repository serve as a container template for smaller repos with microservices meant to act as
a home automation system with Raspberry PI as the main hub.

# Overview

This repository consist of few (for now) microservices.

* **[FastAPI plants control](https://github.com/DanielKusyDev/fastapi-rpi-plants-control)** app to managing humidity, light and temperature sensors as a part of plants growth automation
* **[FastAPI gateway](https://github.com/DanielKusyDev/rpi-gateway)** serving as a main connector between other microservices and the frontend app
* ... more services in the future
* **[Django Authentication](https://github.com/DanielKusyDev/django-auth-microservice)** service to perform AAA tasks 
* **[Email microservice](https://github.com/DanielKusyDev/microservice-email)** in Go used by auth service