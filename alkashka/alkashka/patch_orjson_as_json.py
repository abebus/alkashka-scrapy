import json as std_json
from typing import TYPE_CHECKING, Any

import orjson

# Mapping json kwargs to orjson options
JSON_TO_ORJSON_OPTIONS = {
    "indent": orjson.OPT_INDENT_2,  # maps indent to OPT_INDENT_2 (note: no control over indent size)
    "sort_keys": orjson.OPT_SORT_KEYS,
    "default": "default",  # handle separately
    # orjson does not support: skipkeys, ensure_ascii, check_circular, allow_nan, separators
}

UNSUPPORTED_KWARGS = {
    "skipkeys",
    "ensure_ascii",
    "check_circular",
    "allow_nan",
    "separators",
    "cls",
}


def dumps(
    obj,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw,
) -> str:
    # Check for unsupported kwargs
    unsupported_used = any(
        locals()[k]
        for k in UNSUPPORTED_KWARGS
        if k in locals() and locals()[k] not in (False, None)
    )

    # If unsupported kwargs are used, fall back to std json
    if unsupported_used or kw:
        return std_json.dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw,
        )

    # Build options bitmask
    option = 0
    if indent is not None:
        option |= orjson.OPT_INDENT_2
    if sort_keys:
        option |= orjson.OPT_SORT_KEYS

    try:
        return orjson.dumps(obj, default=default, option=option).decode("utf-8")
    except (TypeError, orjson.JSONEncodeError):
        return std_json.dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw,
        )


def loads(s: bytes | bytearray | memoryview | str) -> Any:
    try:
        return orjson.loads(s)
    except orjson.JSONDecodeError:
        return std_json.loads(s)


if not TYPE_CHECKING:  # ignore mypy errors
    # Monkey patch
    std_json.dumps = dumps
    std_json.loads = loads

    import sys

    # Ensure sys.modules has the patched json
    sys.modules["json"].dumps = dumps
    sys.modules["json"].loads = loads
