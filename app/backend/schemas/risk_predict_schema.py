"""Schema helpers for late-shipment prediction requests."""


def normalize_records(payload: dict) -> list[dict]:
    if "records" in payload and isinstance(payload["records"], list):
        return payload["records"]
    if "data" in payload and isinstance(payload["data"], list):
        return payload["data"]
    if "data" in payload and isinstance(payload["data"], dict):
        return [payload["data"]]
    return [payload]
