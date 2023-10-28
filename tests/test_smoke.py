import repoctx


def test_package_imports():
    assert repoctx is not None


def test_version_is_a_string():
    assert isinstance(repoctx.__version__, str)
    assert repoctx.__version__.count(".") >= 2
