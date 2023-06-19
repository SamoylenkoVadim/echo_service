from typing import Union


def make_endpoint_name(endpoint_id: Union[int, str]) -> str:
    return f"endpoint_{endpoint_id}"
