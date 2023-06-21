import re


def validate_path(path: str) -> str:
    pattern = "^/[a-zA-Z0-9_/]+$"
    if not re.match(pattern, path):
        raise ValueError(
            "Invalid URL path format. path_pattern: ^/[a-zA-Z0-9_/]+$",
        )
    return path


def validate_code(code: int) -> int:
    if code < 100 or code > 599:
        raise ValueError("Invalid HTTP code. Must be between 100 and 599.")
    return code
