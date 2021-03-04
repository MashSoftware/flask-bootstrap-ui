# Flask Bootstrap UI Template

This template repository contains a Flask app using the Bootstrap UI framework. The app is structured based on best practices and my personal learning and experience gained on previous projects. Using a template repository you can generate a new repository with the same directory structure and files to start a new project quickly.

## Prerequisites

### Required

- Python 3.6.x or higher

### Optional

- Redis 4.0.x or higher (for rate limiting, otherwise in-memory storage is used)

## Getting started

### Create venv and install requirements

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Run app

```shell
flask run
```

## Testing

Run the test suite

```shell
pytest
```
