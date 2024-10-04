import pytest


@pytest.fixture
def sample_files() -> dict[str, str]:
    """A small multi-module project used across several tests."""
    return {
        "app/config.py": (
            "def load_config(path):\n"
            '    """Read and parse a JSON config file."""\n'
            "    import json\n"
            "    return json.loads(open(path).read())\n"
        ),
        "app/server.py": (
            "from app.config import load_config\n"
            "\n"
            "class Server:\n"
            "    def start(self, port):\n"
            '        """Start the HTTP server on a port."""\n'
            "        return port\n"
            "\n"
            "    def stop(self):\n"
            "        return None\n"
        ),
        "app/utils.py": (
            "def slugify(text):\n"
            '    """Turn a string into a url slug."""\n'
            "    return text.lower().replace(' ', '-')\n"
        ),
    }
