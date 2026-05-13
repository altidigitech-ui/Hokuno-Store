"""Thin Printify Admin API client."""
import time
from typing import Iterator

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import config


class PrintifyError(RuntimeError):
    pass


def _headers():
    config.require_printify_token()
    return {
        "Authorization": f"Bearer {config.PRINTIFY_TOKEN}",
        "User-Agent": "Hokuno-Mockup-Pipeline/1.0",
        "Accept": "application/json",
    }


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=8),
    retry=retry_if_exception_type((requests.RequestException, PrintifyError)),
)
def _get(path: str, params=None):
    url = f"{config.PRINTIFY_BASE_URL}{path}"
    r = requests.get(url, headers=_headers(), params=params, timeout=30)
    if r.status_code == 429:
        raise PrintifyError(f"Throttled: {r.text[:200]}")
    if r.status_code >= 500:
        raise PrintifyError(f"Server error {r.status_code}: {r.text[:200]}")
    r.raise_for_status()
    return r.json()


def iter_products(shop_id: str | None = None, limit: int = 50) -> Iterator[dict]:
    """Yield every product across paginated /products.json."""
    shop_id = shop_id or config.PRINTIFY_SHOP_ID
    page = 1
    while True:
        data = _get(
            f"/shops/{shop_id}/products.json",
            params={"page": page, "limit": limit},
        )
        for product in data.get("data", []):
            yield product
        last_page = data.get("last_page") or page
        if page >= last_page:
            return
        page += 1
        time.sleep(config.PRINTIFY_DELAY_S)


def list_all_products(shop_id: str | None = None) -> list[dict]:
    return list(iter_products(shop_id=shop_id))


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=8),
    retry=retry_if_exception_type(requests.RequestException),
)
def download_image(url: str) -> bytes:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content
