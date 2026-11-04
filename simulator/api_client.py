from urllib import request
from urllib.error import HTTPError, URLError
import json


API_BASE_URL = "http://127.0.0.1:8000"


def post_json(path: str, payload: dict[str, object]) -> dict[str, object]:
    url = API_BASE_URL + path

    body = json.dumps(payload).encode("utf-8")

    url_request = request.Request(
        url=url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(url_request) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body)

    except HTTPError as error:
        error_body = error.read().decode("utf-8")

        print(f"HTTP error when POSTing to {url}")
        print(f"Status code: {error.code}")
        print(f"Response body: {error_body}")

        raise

    except URLError as error:
        print(f"Could not connect to backend at {API_BASE_URL}")
        print(f"Reason: {error.reason}")

        raise
