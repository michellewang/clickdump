"""Value serialization for JSON compatibility."""

from __future__ import annotations

import base64
from enum import Enum
from typing import Any


def serialize_value(value: Any, _seen: set[int] | None = None) -> Any:
    """Serialize a value for JSON compatibility."""
    if _seen is None:
        _seen = set()

    if value is None:
        return None

    if isinstance(value, (bool, int, float, str)):
        return value

    obj_id = id(value)
    if obj_id in _seen:
        return {"__circular_ref__": True}

    if isinstance(value, (list, tuple)):
        return _serialize_sequence(value, _seen, obj_id)

    if isinstance(value, dict):
        return _serialize_dict(value, _seen, obj_id)

    if isinstance(value, set):
        return _serialize_set(value, _seen, obj_id)

    if isinstance(value, frozenset):
        return _serialize_frozenset(value, _seen, obj_id)

    if isinstance(value, Enum):
        return _serialize_enum(value)

    if isinstance(value, bytes):
        return _serialize_bytes(value)

    if isinstance(value, range):
        return {"__range__": [value.start, value.stop, value.step]}

    if isinstance(value, type):
        return {"__type__": True, "name": value.__name__, "module": value.__module__}

    return {
        "__repr__": repr(value),
        "__type_name__": type(value).__name__,
        "__serializable__": False,
    }


def _serialize_sequence(value: Any, seen: set[int], obj_id: int) -> list[Any]:
    seen.add(obj_id)
    result = [serialize_value(v, seen) for v in value]
    seen.discard(obj_id)
    return result


def _serialize_dict(
    value: dict[Any, Any], seen: set[int], obj_id: int
) -> dict[str, Any]:
    seen.add(obj_id)
    result = {str(k): serialize_value(v, seen) for k, v in value.items()}
    seen.discard(obj_id)
    return result


def _serialize_set(
    value: set[Any], seen: set[int], obj_id: int
) -> dict[str, list[Any]]:
    seen.add(obj_id)
    result: dict[str, list[Any]] = {
        "__set__": [serialize_value(v, seen) for v in sorted(value, key=str)]
    }
    seen.discard(obj_id)
    return result


def _serialize_frozenset(
    value: frozenset[Any], seen: set[int], obj_id: int
) -> dict[str, list[Any]]:
    seen.add(obj_id)
    result: dict[str, list[Any]] = {
        "__frozenset__": [serialize_value(v, seen) for v in sorted(value, key=str)]
    }
    seen.discard(obj_id)
    return result


def _serialize_enum(value: Enum) -> dict[str, Any]:
    return {
        "__enum__": True,
        "class": type(value).__name__,
        "module": type(value).__module__,
        "value": serialize_value(value.value),
        "name": value.name,
    }


def _serialize_bytes(value: bytes) -> dict[str, str]:
    try:
        return {"__bytes__": value.decode("utf-8")}
    except UnicodeDecodeError:
        return {"__bytes_b64__": base64.b64encode(value).decode("ascii")}
