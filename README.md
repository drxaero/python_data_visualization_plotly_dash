# Docker Deployment of a `Dash` App

## Introduction

This is my final project of Udemy course [Python Data Visualization: Dashboards with Plotly & Dash](https://www.udemy.com/course-dashboard-redirect/?course_id=5157698).
This repository demonstrates the docker deployment of a [Dash](https://dash.plotly.com/) dashboard.

## To deploy this app

To build the docker image, run:
```bash
docker build -t py_dash:1.0 .
```

To run the docker container:
```bash
docker run -it -p 8091:8091 --name py_dash_app py_dash:1.0
```

# To check the health of the deployed app

Hit up the '/ping' endpoint with a GET request on the server that's up and running.
