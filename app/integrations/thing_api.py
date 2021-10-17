import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from flask_login import UserMixin
from werkzeug.exceptions import (
    InternalServerError,
    NotFound,
    RequestTimeout,
    TooManyRequests,
    Unauthorized,
)


class ThingAPI:
    def __init__(self):
        self.url = current_app.config["THING_API_URL"]
        self.version = current_app.config["THING_API_VERSION"]
        self.timeout = current_app.config["TIMEOUT"]


class Thing(ThingAPI):
    def create(self, token, name, colour):
        """Create a new Thing."""
        url = f"{self.url}/{self.version}/things"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
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
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, token, filters, format="json"):
        """Get a list of Things."""
        if filters:
            qs = urlencode(filters)
            url = f"{self.url}/{self.version}/things?{qs}"
        else:
            url = f"{self.url}/{self.version}/things"

        if format == "csv":
            headers = {"Accept": "text/csv", "Authorization": f"Bearer {token}"}
        else:
            headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

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
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, token, thing_id):
        """Get a Thing with a specific ID."""
        url = f"{self.url}/{self.version}/things/{thing_id}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

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
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, token, thing_id, name, colour):
        """Edit a Thing with a specific ID."""
        url = f"{self.url}/{self.version}/things/{thing_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
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
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, token, thing_id):
        """Delete a Thing with a specific ID."""
        url = f"{self.url}/{self.version}/things/{thing_id}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError


class User(UserMixin, ThingAPI):
    def create(self, email_address, password):
        """Create a new User."""
        url = f"{self.url}/{self.version}/users"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_user = {"email_address": email_address, "password": password}

        try:
            response = requests.post(url, data=json.dumps(new_user), headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 201:
                user = json.loads(response.text)
                user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if user["updated_at"]:
                    user["updated_at"] = datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return user
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, token, filters, format="json"):
        """Get a list of Users."""
        if filters:
            qs = urlencode(filters)
            url = f"{self.url}/{self.version}/users?{qs}"
        else:
            url = f"{self.url}/{self.version}/users"

        if format == "csv":
            headers = {"Accept": "text/csv", "Authorization": f"Bearer {token}"}
        else:
            headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

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
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, token, user_id):
        """Get a User with a specific ID."""
        url = f"{self.url}/{self.version}/users/{user_id}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                user = json.loads(response.text)
                user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if user["updated_at"]:
                    user["updated_at"] = datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return user
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, token, user_id, email_address, password):
        """Edit a User with a specific ID."""
        url = f"{self.url}/{self.version}/users/{user_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        changed_user = {"email_address": email_address, "password": password}

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_user),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                user = json.loads(response.text)
                user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if user["updated_at"]:
                    user["updated_at"] = datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return user
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, token, user_id):
        """Delete a User with a specific ID."""
        url = f"{self.url}/{self.version}/users/{user_id}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError


@login_manager.user_loader
def load_user(user_id):
    """Get a User with a specific ID."""
    url = f"{current_app.config['THING_API_URL']}/{current_app.config['THING_API_VERSION']}/users/{user_id}"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {request.cookies.get('token')}"}

    try:
        response = requests.get(url, headers=headers, timeout=current_app.config["TIMEOUT"])
    except requests.exceptions.Timeout:
        raise RequestTimeout
    else:
        if response.status_code == 200:
            user = json.loads(response.text)
            user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
            if user["updated_at"]:
                user["updated_at"] = datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
            return user
        else:
            return None


class Auth(ThingAPI):
    def login(self, email_address, password):
        """Authenticate a user using HTTP Basic Auth and return a HTTP Bearer Token"""
        url = f"{self.url}/{self.version}/auth/token"
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                auth=(email_address, password),
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                token = json.loads(response.text)
                return token
            elif response.status_code == 401:
                raise Unauthorized
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError
