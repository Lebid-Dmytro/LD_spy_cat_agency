import functools
from typing import Set

import requests
from django.conf import settings


@functools.lru_cache(maxsize=1)
def fetch_valid_breeds() -> Set[str]:
    """Return cat breeds from TheCatAPI and cache the result to avoid extra calls."""
    url = getattr(settings, "CAT_API_URL", "https://api.thecatapi.com/v1/breeds")
    headers = {}
    if getattr(settings, "CAT_API_KEY", ""):
        headers["x-api-key"] = settings.CAT_API_KEY
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    names = {str(item.get("name")).strip() for item in data if "name" in item}
    return {n for n in names if n}
