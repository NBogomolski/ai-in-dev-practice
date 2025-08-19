import requests
from typing import Any, Dict, List

FAKESTORE_PRODUCTS_URL = "https://fakestoreapi.com/products"


def fetch_products(timeout_seconds: float = 10.0) -> List[Dict[str, Any]]:
	"""Fetch products from Fake Store API.

	Args:
		timeout_seconds: Request timeout in seconds.

	Returns:
		List of product dicts.

	Raises:
		requests.RequestException: If the HTTP request fails.
		ValueError: If the response JSON is not a list.
	"""
	response = requests.get(FAKESTORE_PRODUCTS_URL, timeout=timeout_seconds)
	response.raise_for_status()
	data = response.json()
	if not isinstance(data, list):
		raise ValueError("Expected a list of products from the API")

	# to test with mock item
	# data[0]["price"] = -1
	
	return data
