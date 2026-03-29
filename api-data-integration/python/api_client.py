"""Minimal REST client that hydrates public endpoints for the pipeline."""

from typing import Any, Dict, Iterable, List, Optional

import requests


class APIClient:
    """Wraps the JSONPlaceholder endpoints with pagination and error handling."""

    BASE_URL = "https://jsonplaceholder.typicode.com"
    _PAGE_SIZE = 50

    def __init__(self, session: Optional[requests.Session] = None):
        self._session = session or requests.Session()

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        response = self._session.get(url, params=params, timeout=10)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(f"API request failed {response.status_code} for {url}") from exc
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError("Unable to parse JSON response") from exc

    def _paginate(self, path: str) -> Iterable[Dict[str, Any]]:
        page = 1
        while True:
            params = {"_page": page, "_limit": self._PAGE_SIZE}
            payload = self._request(path, params=params)
            if not payload:
                break
            for item in payload:
                yield item
            if len(payload) < self._PAGE_SIZE:
                break
            page += 1

    def fetch_users(self) -> List[Dict[str, Any]]:
        return [self._normalize_user(u) for u in self._paginate("users")]

    def fetch_posts(self) -> List[Dict[str, Any]]:
        return [self._normalize_post(p) for p in self._paginate("posts")]

    @staticmethod
    def _normalize_user(raw: Dict[str, Any]) -> Dict[str, Any]:
        address = raw.get("address", {})
        company = raw.get("company", {})
        return {
            "user_id": raw.get("id"),
            "name": raw.get("name"),
            "username": raw.get("username"),
            "email": raw.get("email"),
            "city": address.get("city"),
            "company_name": company.get("name"),
        }

    @staticmethod
    def _normalize_post(raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "external_id": raw.get("id"),
            "user_id": raw.get("userId"),
            "title": raw.get("title"),
            "body": raw.get("body"),
        }
