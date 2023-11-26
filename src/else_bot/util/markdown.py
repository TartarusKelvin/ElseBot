import re


def get_links(text: str) -> list[tuple]:
    pattern = r"\[(.*)\]\((https:\/\/.*)\)"
    return re.findall(pattern, text)
