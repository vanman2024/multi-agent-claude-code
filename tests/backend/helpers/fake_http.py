from __future__ import annotations

from typing import Any, Dict, Tuple

import httpx


class FakeAsyncClient:
    """A minimal async-compatible httpx-like client for tests.

    routes: maps (method.upper(), path) -> response
    response can be:
      - dict/list (JSON), implies status=200
      - tuple(status_code, json)
    """

    def __init__(self, routes: Dict[Tuple[str, str], Any] | None = None) -> None:
        self._routes: Dict[Tuple[str, str], Any] = routes or {}
        self.requests: list[Tuple[str, str, Any]] = []

    def register(self, method: str, path: str, response: Any) -> None:
        self._routes[(method.upper(), path)] = response

    def clear(self) -> None:
        self._routes.clear()
        self.requests.clear()

    async def __aenter__(self) -> "FakeAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: D401
        return None

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self._request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self._request("POST", url, **kwargs)

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        method_u = method.upper()
        path = url
        self.requests.append((method_u, path, kwargs))
        data = self._routes.get((method_u, path))
        status = 200
        json_data: Any | None = None
        if isinstance(data, tuple) and len(data) == 2:
            status, json_data = data
        else:
            json_data = data

        req = httpx.Request(method_u, path)
        if json_data is None:
            return httpx.Response(status, request=req)
        return httpx.Response(status, request=req, json=json_data)

