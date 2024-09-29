import pytest

from repoctx.config import Config


def test_defaults_are_offline():
    config = Config()
    assert config.embedder == "hashing"
    assert config.embedding_dim > 0
    assert config.include_ext == (".py",)


def test_invalid_alpha_raises():
    with pytest.raises(ValueError):
        Config(alpha=2.0)


def test_invalid_dim_raises():
    with pytest.raises(ValueError):
        Config(embedding_dim=0)


def test_to_dict_roundtrip():
    data = Config(embedding_dim=128).to_dict()
    assert data["embedding_dim"] == 128


def test_from_env(monkeypatch):
    monkeypatch.setenv("REPOCTX_EMBEDDING_DIM", "99")
    monkeypatch.setenv("REPOCTX_ALPHA", "0.3")
    config = Config.from_env()
    assert config.embedding_dim == 99
    assert abs(config.alpha - 0.3) < 1e-9
