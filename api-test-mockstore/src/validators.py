from typing import Any, Dict, List, Tuple


class ValidationIssue:
	"""Represents a single validation issue for a product."""

	def __init__(self, field_path: str, message: str) -> None:
		self.field_path = field_path
		self.message = message

	def __repr__(self) -> str:  # pragma: no cover - cosmetic
		return f"ValidationIssue(field_path={self.field_path!r}, message={self.message!r})"

	def to_dict(self) -> Dict[str, str]:
		return {"field": self.field_path, "message": self.message}


def validate_product(product: Dict[str, Any]) -> List[ValidationIssue]:
	"""Validate a single product returning a list of issues (empty if valid)."""
	issues: List[ValidationIssue] = []

	# title must exist and not be empty
	title = product.get("title")
	if not isinstance(title, str) or not title.strip():
		issues.append(ValidationIssue("title", "must be a non-empty string"))

	# price must exist and not be negative
	price = product.get("price")
	if not isinstance(price, (int, float)):
		issues.append(ValidationIssue("price", "must be a number"))
	else:
		if price < 0:
			issues.append(ValidationIssue("price", "must not be negative"))

	# rating.rate must not exceed 5
	rating = product.get("rating")
	if not isinstance(rating, dict):
		issues.append(ValidationIssue("rating", "must be an object with 'rate'"))
	else:
		rate = rating.get("rate")
		if not isinstance(rate, (int, float)):
			issues.append(ValidationIssue("rating.rate", "must be a number"))
		else:
			if rate > 5:
				issues.append(ValidationIssue("rating.rate", "must not exceed 5"))

	return issues


def find_defective_products(products: List[Dict[str, Any]]) -> List[Tuple[int, Dict[str, Any], List[ValidationIssue]]]:
	"""Return products with any validation issues.

	Returns a list of tuples: (index, product, issues)
	"""
	defectives: List[Tuple[int, Dict[str, Any], List[ValidationIssue]]] = []
	for index, product in enumerate(products):
		issues = validate_product(product)
		if issues:
			defectives.append((index, product, issues))
	return defectives
