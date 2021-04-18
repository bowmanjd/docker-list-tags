#!/usr/bin/env python3

"""List and process image tags for a repository in a Docker v2 registry."""


import json
import typing
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from email.message import Message

REGISTRIES = {
    "docker.io": "index.docker.io",
}


@dataclass
class Response:
    """Container for HTTP response."""

    body: str
    headers: Message
    status: int
    error_count: int = 0

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        return json.loads(self.body)


def request(
    url: str,
    data: dict = None,
    headers: dict = None,
    method: str = "get",
    error_count: int = 0,
) -> Response:
    """
    Perform HTTP request.

    Args:
        url: url to fetch
        data: dict of keys/values to be form encoded
        headers: optional dict of request headers
        method: HTTP method , such as GET or POST
        error_count: optional current count of HTTP errors, to manage recursion

    Returns:
        A dict with headers, body, status code, and, if applicable, object
        rendered from JSON
    """
    method = method.casefold()
    request_data = None
    if data:
        form_encoded = urllib.parse.urlencode(data, doseq=True, safe="/")
        if method == "get":
            url += f"?{form_encoded}"
        else:
            request_data = form_encoded.encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers or {}, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body="", headers=e.headers, status=e.code, error_count=error_count + 1
        )

    return response


def www_authenticate(headers: Message) -> dict:
    """
    Parse Www-Authenticate header.

    Args:
        headers: header mapping from HTTP response

    Returns:
        A dict with realm, service, etc.
    """
    www_auth = headers["www-authenticate"]
    parameter_string = www_auth.split(None, 1)[-1]
    splits = (x.split("=") for x in parameter_string.split(","))
    info = {x[0]: x[1].strip('"') for x in splits}
    return info


def registry_request(
    endpoint: str, token: str = None, registry: str = "docker.io", error_count: int = 0
) -> typing.Any:
    """
    Perform API request to docker-compatible registry.

    Args:
        endpoint: API endpoint path
        token: authorization token string
        registry: name of registry, such as docker.io (default) or quay.io
        error_count: optional current count of HTTP errors, for controlled nesting

    Returns:
        A list or dict rendered from the JSON
    """
    registry = REGISTRIES.get(registry, registry)
    url = f"https://{registry}/v2/{endpoint}"
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = request(url, headers=headers)
    if response.status == 401:
        auth_info = www_authenticate(response.headers)
        url = (
            f"{auth_info['realm']}?"
            f"service={auth_info['service']}&scope={auth_info['scope']}"
        )
        token_response = request(url).json()
        token = token_response["token"]
        if response.error_count <= 3:
            response = registry_request(endpoint, token, registry, response.error_count)
    return response


def list_tags(
    image_name: str, repo: str = "library", registry: str = "docker.io"
) -> list:
    """
    List all tags of a given Docker image.

    Args:
        image_name: name of the image
        repo: name of the repository
        registry: name of registry, such as docker.io (default) or quay.io

    Returns:
        A list or dict rendered from the JSON
    """
    response = registry_request(f"{repo}/{image_name}/tags/list", registry=registry)
    return response.json().get("tags")


if __name__ == "__main__":
    print("\n".join(list_tags("alpine")))
