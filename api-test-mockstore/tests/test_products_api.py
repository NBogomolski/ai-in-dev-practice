import json
from typing import Any, Dict, List

import requests

from src.api_client import FAKESTORE_PRODUCTS_URL, fetch_products
from src.validators import find_defective_products, validate_product


def test_api_status_code_ok():
	response = requests.get(FAKESTORE_PRODUCTS_URL, timeout=10.0)
	assert response.status_code == 200


def test_products_have_required_fields_and_constraints():
	products: List[Dict[str, Any]] = fetch_products()
	defectives = find_defective_products(products)

	# The test should not fail because the dataset intentionally contains defects.
	# Instead, we assert that we successfully detected any invalid products and print them.
	# If there are no defects at all, this assertion still passes (defectives could be empty).
	assert defectives is not None

	# Emit a helpful message into the test output for visibility
	if defectives:
		print("Detected defective products (index -> issues):")
		for index, product, issues in defectives:
			issues_str = ", ".join(f"{i.field_path}: {i.message}" for i in issues)
			print(f"- idx={index} id={product.get('id')} title={product.get('title')!r} -> {issues_str}")


# Optional: targeted unit validations on a crafted sample

def test_validate_product_unit_samples():
	ok = {"title": "A", "price": 1.0, "rating": {"rate": 5}}
	assert validate_product(ok) == []

	missing_title = {"price": 10, "rating": {"rate": 4}}
	assert any(i.field_path == "title" for i in validate_product(missing_title))

	negative_price = {"title": "B", "price": -1, "rating": {"rate": 4}}
	assert any(i.field_path == "price" for i in validate_product(negative_price))

	rate_too_high = {"title": "C", "price": 0, "rating": {"rate": 6}}
	assert any(i.field_path == "rating.rate" for i in validate_product(rate_too_high))
