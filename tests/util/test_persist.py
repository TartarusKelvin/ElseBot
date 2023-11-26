import pytest
import uuid
import else_bot.util.persist as persist
import pathlib


def test_basic_func(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / str(uuid.uuid4())
    d = persist.PersistedDict(path)
    d["test"] = 10
    d["other"] = 20
    assert d["test"] == 10
    assert d["other"] == 20

    d2 = persist.PersistedDict(path)
    assert d2["test"] == 10
    assert d2["other"] == 20

    del d2["other"]

    d3 = persist.PersistedDict(pathlib.Path(path))
    with pytest.raises(KeyError):
        d3["other"]
    assert d3["test"] == 10
