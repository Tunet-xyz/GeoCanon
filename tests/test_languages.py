"""Tests for geo_canon.languages"""

from geo_canon.languages import (
    JURISDICTION_LANGUAGE,
    LANGUAGE_CHOICES,
    get_language_choices,
    get_language_for_jurisdiction,
)


class TestLanguages:
    def test_language_choices_not_empty(self):
        assert len(LANGUAGE_CHOICES) > 30

    def test_language_choices_sorted(self):
        labels = [str(choice[1]) for choice in LANGUAGE_CHOICES]
        assert labels == sorted(labels)

    def test_language_for_romania(self):
        assert get_language_for_jurisdiction("Romania") == "ro"

    def test_language_for_germany(self):
        assert get_language_for_jurisdiction("Germany") == "de"

    def test_language_for_japan(self):
        assert get_language_for_jurisdiction("Japan") == "ja"

    def test_language_for_uk(self):
        assert get_language_for_jurisdiction("United Kingdom") == "en"

    def test_language_for_unknown(self):
        assert get_language_for_jurisdiction("Narnia") is None

    def test_get_language_choices_returns_list(self):
        choices = get_language_choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)

    def test_jurisdiction_language_mapping_not_empty(self):
        assert len(JURISDICTION_LANGUAGE) > 100
