"""Schema helpers for supplier-selection requests."""


def parse_bool(value, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def parse_limit(value, default: int = 10, maximum: int = 100) -> int:
    try:
        limit = int(value)
    except (TypeError, ValueError):
        limit = default
    return max(1, min(limit, maximum))
