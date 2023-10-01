import pytest

class TestLineSimple:

    def test_short_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, f"your phrase is {len(phrase)} characters, the test expects 15 or less"











