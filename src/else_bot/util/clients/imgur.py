"""
Module to handle getting album info and images from imgur.com

see: https://apidocs.imgur.com/
"""

import requests
import json
from io import BytesIO


class ImgurClient:
    def __init__(self, *, id: str, secret: str | None) -> None:
        self._ci = id
        self._cs = secret  # unsused for now, we dont need it for public requests
        self._s = requests.Session()
        self._s.headers.update({"Authorization": f"Client-Id {self._ci}"})

    def get_album_images(self, album_id: str) -> list[str]:
        "Given an album id return a list of all images direct links"
        data = json.loads(
            self._s.get(f"https://api.imgur.com/3/album/{album_id}/images").text
        )
        return [x["link"] for x in data["data"]]

    def get_image_as_buffer(self, image_link: str) -> BytesIO:
        "Get image as bytes io buffer"
        return BytesIO(self._s.get(image_link, stream=True).content)
