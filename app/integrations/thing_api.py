import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from werkzeug.exceptions import (
    InternalServerError,
    NotFound,
    RequestTimeout,
    TooManyRequests,
)


class ThingAPI:
    def __init__(self):
        self.url = current_app.config["THING_API_URL"]
        self.version = current_app.config["THING_API_VERSION"]
        self.timeout = current_app.config["TIMEOUT"]

    def list(self, **kwargs):
        """Get a list of Things."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/things?{2}".format(self.url, self.version, qs)
        else:
            url = "{0}/{1}/things".format(self.url, self.version)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                things = json.loads(response.text)
                for thing in things:
                    thing["created_at"] = datetime.strptime(thing["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if thing["updated_at"]:
                        thing["updated_at"] = datetime.strptime(thing["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return things
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def create(self, name):
        """Create a new Thing."""
        url = "{0}/{1}/things".format(self.url, self.version)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_thing = {"name": name}

        try:
            response = requests.post(url, data=json.dumps(new_thing), headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 201:
                thing = json.loads(response.text)
                thing["created_at"] = datetime.strptime(thing["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if thing["updated_at"]:
                    thing["updated_at"] = datetime.strptime(thing["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return thing
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def view(self, thing_id):
        """View a Thing with a specific ID."""
        url = "{0}/{1}/things/{2}".format(self.url, self.version, thing_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                thing = json.loads(response.text)
                thing["created_at"] = datetime.strptime(thing["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if thing["updated_at"]:
                    thing["updated_at"] = datetime.strptime(thing["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return thing
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, thing_id, name):
        """Edit a Thing with a specific ID."""
        url = "{0}/{1}/things/{2}".format(self.url, self.version, thing_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_thing = {"name": name}

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_thing),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                thing = json.loads(response.text)
                thing["created_at"] = datetime.strptime(thing["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if thing["updated_at"]:
                    thing["updated_at"] = datetime.strptime(thing["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return thing
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, thing_id):
        """Delete a Thing with a specific ID."""
        url = "{0}/{1}/things/{2}".format(self.url, self.version, thing_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError
