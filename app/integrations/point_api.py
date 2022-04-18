import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from werkzeug.exceptions import InternalServerError, NotFound, RequestTimeout, TooManyRequests


class PointAPI:
    def __init__(self):
        self.url = current_app.config["POINT_API_URL"]
        self.timeout = current_app.config["TIMEOUT"]


class Point(PointAPI):
    def create(self, name, geometry):
        """Create a new Point."""
        url = f"{self.url}/points"
        headers = {
            "Accept": "application/geo+json",
            "Content-Type": "application/geo+json",
        }
        new_point = {
            "type": "Feature",
            "properties": {"name": name},
            "geometry": json.loads(geometry),
        }

        try:
            response = requests.post(url, data=json.dumps(new_point), headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 201:
                point = json.loads(response.text)
                point["properties"]["created_at"] = datetime.strptime(
                    point["properties"]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                if point["properties"]["updated_at"]:
                    point["properties"]["updated_at"] = datetime.strptime(
                        point["properties"]["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                return point
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, filters, format="json"):
        """Get a list of Points."""
        if filters:
            qs = urlencode(filters)
            url = f"{self.url}/points?{qs}"
        else:
            url = f"{self.url}/points"

        if format == "csv":
            headers = {"Accept": "text/csv"}
        else:
            headers = {"Accept": "application/geo+json"}

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

    def get(self, point_id):
        """Get a Point with a specific ID."""
        url = f"{self.url}/points/{point_id}"
        headers = {"Accept": "application/geo+json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                point = json.loads(response.text)
                point["properties"]["created_at"] = datetime.strptime(
                    point["properties"]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                if point["properties"]["updated_at"]:
                    point["properties"]["updated_at"] = datetime.strptime(
                        point["properties"]["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                return point
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, point_id, name, geometry):
        """Edit a Point with a specific ID."""
        url = f"{self.url}/points/{point_id}"
        headers = {
            "Accept": "application/geo+json",
            "Content-Type": "application/geo+json",
        }
        changed_point = {
            "type": "Feature",
            "properties": {"name": name},
            "geometry": json.loads(geometry),
        }

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_point),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        else:
            if response.status_code == 200:
                point = json.loads(response.text)
                point["properties"]["created_at"] = datetime.strptime(
                    point["properties"]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                if point["properties"]["updated_at"]:
                    point["properties"]["updated_at"] = datetime.strptime(
                        point["properties"]["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                return point
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, point_id):
        """Delete a Point with a specific ID."""
        url = f"{self.url}/points/{point_id}"
        headers = {"Accept": "application/geo+json"}

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
