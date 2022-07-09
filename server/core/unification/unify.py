import re


def parse_value(value_string: str) -> tuple[str, str]:
    """
    Values are of format Integration[End Point]
    :param value_string: string containing the value
    :return: parsed value string
    """
    # ignore warning
    if not re.compile(r"[a-zA-Z]+\[[a-zA-Z\s\d]+\]").fullmatch(value_string):  # noqa
        raise ValueError(f"Invalid value string {value_string}")
    try:
        segments = value_string.split("[")
        assert len(segments) == 2
        assert segments[1].endswith("]")
        integration = segments[0]
        endpoint = segments[1][:-1]
        return integration, endpoint
    except AssertionError:
        raise ValueError(f"Invalid value string {value_string}")
