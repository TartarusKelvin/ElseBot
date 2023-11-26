import pytest
import else_bot.util.clients.scryfall as scryfall
import itertools


class MockScryfallResponse:
    def __init__(self, *, ok=True, ambiguous=False):
        self.ok = ok
        self.ambiguous = ambiguous

    def json(self) -> dict:
        if self.ok:
            return {
                "object": "card",
                "image_uris": {
                    "small": "small_url",
                    "normal": "normal_url",
                    "large": "large_url",
                    "png": "png_url",
                    "art_crop": "art_crop_url",
                    "border_crop": "border_crop_url",
                },
            }
        return (
            {"object": "error"}
            if not self.ambiguous
            else {"object": "error", "type": "ambiguous"}
        )


@pytest.mark.parametrize(
    "image_type,exact",
    itertools.product(
        ["small", "normal", "large", "png", "art_crop", "border_crop"], (True, False)
    ),
)
def test_card_lookup_match_ok(monkeypatch, image_type, exact):
    def mock_get(*args, **kwargs):
        return MockScryfallResponse(ok=True)

    monkeypatch.setattr(scryfall.requests, "get", mock_get)
    sc = scryfall.ScryfallClient()
    assert (
        sc.lookup_card_image("jace", image_type=image_type, exact=exact)
        == image_type + "_url"
    ), "Incorrect Image Uurl Returned"


def test_card_lookup_match_ambigous(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockScryfallResponse(ok=False, ambiguous=True)

    monkeypatch.setattr(scryfall.requests, "get", mock_get)
    sc = scryfall.ScryfallClient()
    with pytest.raises(scryfall.TooManyMatches):
        sc.lookup_card_image("jace", exact=True)


def test_card_lookup_no_match(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockScryfallResponse(ok=False, ambiguous=False)

    monkeypatch.setattr(scryfall.requests, "get", mock_get)
    sc = scryfall.ScryfallClient()
    with pytest.raises(scryfall.NoMatch):
        sc.lookup_card_image("jace", exact=True)
