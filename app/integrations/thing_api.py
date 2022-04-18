import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from werkzeug.exceptions import InternalServerError, NotFound, RequestTimeout, TooManyRequests


class ThingAPI:
    def __init__(self):
        self.url = current_app.config["THING_API_URL"]
        self.timeout = current_app.config["TIMEOUT"]


class Thing(ThingAPI):
    def create(self, name, colour):
        """Create a new Thing."""
        url = f"{self.url}/things"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_thing = {"name": name, "colour": colour}

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

    def list(self, filters, format="json"):
        """Get a list of Things."""
        if filters:
            qs = urlencode(filters)
            url = f"{self.url}/things?{qs}"
        else:
            url = f"{self.url}/things"

        if format == "csv":
            headers = {"Accept": "text/csv"}
        else:
            headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                if format == "csv":
                    return response.text
                else:
                    return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, thing_id):
        """Get a Thing with a specific ID."""
        url = f"{self.url}/things/{thing_id}"
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

    def edit(self, thing_id, name, colour):
        """Edit a Thing with a specific ID."""
        url = f"{self.url}/things/{thing_id}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_thing = {"name": name, "colour": colour}

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
        url = f"{self.url}/things/{thing_id}"
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
