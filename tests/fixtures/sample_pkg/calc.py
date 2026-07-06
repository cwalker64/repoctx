def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


class Calculator:
    """A tiny stateful calculator."""

    def __init__(self):
        self.total = 0

    def add(self, value):
        self.total = add(self.total, value)
        return self.total
