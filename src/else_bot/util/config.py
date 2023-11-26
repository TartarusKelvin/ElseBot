"""

"""
import pathlib
import json


class ConfigError(BaseException):
    pass


class InvalidValue(ConfigError):
    pass


class MissingOption(ConfigError):
    pass


class Config:
    def __init__(
        self, *, token, imgur_config, reddit_config, else_channels, custom_magic_channel
    ) -> None:
        self.discord_token = token
        self.imgur_config = imgur_config
        self.reddit_config = reddit_config
        self.else_channels = else_channels
        self.custom_magic_channel = custom_magic_channel

    @classmethod
    def get_config(cls, config_path=None):
        config_path = pathlib.Path(config_path or "config/config.json")
        if config_path.exists():
            config_data = json.loads(config_path.read_text())
            if "token" not in config_data:
                raise MissingOption("token")
            if "else_channels" not in config_data:
                raise MissingOption("else_channels")
            if "custom_magic_channel" not in config_data:
                raise MissingOption("custom_magic_channel")
            imgur_config = ImgurConfig.from_dict(config_data.get("imgur", {}))
            if not imgur_config.is_valid():
                raise InvalidValue("Invlaid Imgur Client Config")
            reddit_config = RedditConfig.from_dict(config_data.get("reddit", {}))
            if not reddit_config.is_valid():
                raise InvalidValue("Invlaid Reddit Client Config")
            return cls(
                token=config_data["token"],
                imgur_config=imgur_config,
                reddit_config=reddit_config,
                else_channels=config_data["else_channels"],
                custom_magic_channel=config_data["custom_magic_channel"],
            )


class ClientConfig:
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    def is_valid(self):
        return self.id and self.secret

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("id"), data.get("secret"))

    def to_dict(self):
        return {"id": self.id, "secret": self.secret}


class ImgurConfig(ClientConfig):
    pass


class RedditConfig(ClientConfig):
    pass
