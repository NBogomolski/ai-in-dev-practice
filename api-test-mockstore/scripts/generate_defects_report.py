#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List

# Allow running from project root or script directory
try:
	from src.api_client import fetch_products
	from src.validators import find_defective_products
except ModuleNotFoundError:
	# When executed as `python scripts/generate_defects_report.py`
	import os
	sys.path.append(os.path.dirname(os.path.dirname(__file__)))
	from src.api_client import fetch_products
	from src.validators import find_defective_products


def main() -> int:
	try:
		products: List[Dict[str, Any]] = fetch_products()
	except Exception as exc:  # broad: report and fail non-zero for CLI
		print(f"Error fetching products: {exc}", file=sys.stderr)
		return 2

	defectives = find_defective_products(products)

	report = []
	for index, product, issues in defectives:
		report.append(
			{
				"index": index,
				"id": product.get("id"),
				"title": product.get("title"),
				"issues": [issue.to_dict() for issue in issues],
			}
		)

	print(json.dumps({"defects": report, "total_products": len(products), "defective_count": len(report)}, indent=2))
	return 0


if __name__ == "__main__":
	sys.exit(main())
