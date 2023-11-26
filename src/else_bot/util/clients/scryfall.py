"""
For getting scryfall cards etc.

See: https://scryfall.com/docs/api
"""
import requests

_urls: dict[str, str] = {"cards_named": "https://api.scryfall.com/cards/named"}
_supported_image_types = [
    "small",
    "normal",
    "large",
    "png",
    "art_crop",
    "border_crop",
]


class ScryfallException(BaseException):
    pass


class NoMatch(ScryfallException):
    pass


class TooManyMatches(ScryfallException):
    pass


class ScryfallClient:
    def __init__(self):
        pass

    def lookup_card_image(
        self, card_name: str, *, exact: bool = True, image_type="border_crop"
    ) -> str:
        """
        Gets a cards image url from scryfall, can either be an exact search (default)
        or a fuzzy search. In the case that no card was found raises NoMatch
        and if more than one card matches raises TooManyMatches
        """
        assert image_type in _supported_image_types, "Unsupported Image Type"
        params = {"exact": card_name} if exact else {"fuzzy": card_name}
        card_data = requests.get(url=_urls["cards_named"], params=params).json()
        if card_data["object"] == "error":
            if card_data.get("type") == "ambiguous":
                raise TooManyMatches
            raise NoMatch
        return card_data["image_uris"][image_type]
