import requests
from starlette.responses import Response


class ForeignAPI:

    BASE_URL = None

    def __init__(self, url: str, **format_kwargs):
        if not self.BASE_URL:
            raise NotImplementedError("BASE_URL is required")

        self.path = url
        self.absolute_url = self.BASE_URL + url.format(**format_kwargs)

    def __str__(self) -> str:
        return self.absolute_url

    def __repr__(self) -> str:
        return self.absolute_url

    def amend_url(self, suffix: str) -> "ForeignAPI":
        """Adds given suffix to the url e.g. https://foo --> https://foo/bar"""
        return self.__class__(self.path + suffix)

    def send_request(self, method: str, url: str, **kwargs) -> Response:
        resp = getattr(requests, method)(url, **kwargs)
        return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

    def get(self, params: dict = None) -> Response:
        return self.send_request("get", url=self.absolute_url, params=params)

    def details(self, *url_params, params: dict = None) -> Response:
        url = "/".join([self.absolute_url, *url_params])
        return self.send_request("get", url=url, params=params)

    def post(self, data: dict = None) -> Response:
        return self.send_request("post", url=self.absolute_url, json=data)

    def put(self, data: dict = None) -> Response:
        return self.send_request("put", url=self.absolute_url, json=data)

    def patch(self, data: dict = None) -> Response:
        return self.send_request("patch", url=self.absolute_url, json=data)

    def delete(self) -> Response:
        return self.send_request(
            "delete",
            url=self.absolute_url,
        )
