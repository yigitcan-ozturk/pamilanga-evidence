from typing import Any


def first_divergence(expected: list[dict], observed: list[dict]) -> dict[str, Any]:
    """Return the earliest event whose type or payload differs.

    This identifies first observable divergence, not root cause.
    """
    limit = min(len(expected), len(observed))
    for index in range(limit):
        baseline = expected[index]
        actual = observed[index]
        if baseline.get("event_type") != actual.get("event_type") or baseline.get("payload") != actual.get("payload"):
            return {
                "status": "FOUND",
                "index": index,
                "baseline_event_id": baseline.get("event_id"),
                "observed_event_id": actual.get("event_id"),
                "time_ns": actual.get("time", {}).get("event_time_ns"),
                "stage": actual.get("event_type"),
                "expected": baseline.get("payload"),
                "observed": actual.get("payload"),
            }

    if len(expected) != len(observed):
        baseline = expected[limit] if len(expected) > limit else None
        actual = observed[limit] if len(observed) > limit else None
        return {
            "status": "FOUND",
            "index": limit,
            "baseline_event_id": baseline.get("event_id") if baseline else None,
            "observed_event_id": actual.get("event_id") if actual else None,
            "time_ns": actual.get("time", {}).get("event_time_ns") if actual else None,
            "stage": actual.get("event_type") if actual else "missing_event",
            "expected": baseline.get("payload") if baseline else None,
            "observed": actual.get("payload") if actual else None,
        }

    return {"status": "NONE"}
