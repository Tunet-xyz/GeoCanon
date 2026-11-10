"""Tests for geo_canon.dial_codes"""

import pytest

from geo_canon.dial_codes import (
    DIAL_CODE_CHOICES,
    PHONE_PATTERNS,
    format_phone_number,
    get_dial_code,
    get_dial_code_choices,
    get_phone_number_type,
    is_phone_extra_available,
    validate_phone,
    validate_phone_number,
)


class TestDialCodes:
    def test_dial_code_choices_not_empty(self):
        assert len(DIAL_CODE_CHOICES) > 100

    def test_get_dial_code_romania(self):
        assert get_dial_code("Romania") == "+40"

    def test_get_dial_code_us(self):
        assert get_dial_code("United States") == "+1"

    def test_get_dial_code_uk(self):
        assert get_dial_code("United Kingdom") == "+44"

    def test_get_dial_code_unknown(self):
        assert get_dial_code("Narnia") is None

    def test_get_dial_code_choices_returns_list(self):
        choices = get_dial_code_choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)


class TestPhoneValidation:
    def test_valid_uk_phone(self):
        assert validate_phone("7123456789", "+44") is True

    def test_invalid_uk_phone_too_short(self):
        assert validate_phone("712345", "+44") is False

    def test_valid_us_phone(self):
        assert validate_phone("2125551234", "+1") is True

    def test_invalid_us_phone(self):
        assert validate_phone("123", "+1") is False

    def test_valid_romania_phone(self):
        assert validate_phone("712345678", "+40") is True

    def test_unknown_dial_code(self):
        assert validate_phone("1234", "+999") is False

    def test_benin_numbers_are_01_and_eight_digits(self):
        assert validate_phone("0197123456", "+229") is True
        assert validate_phone("97123456", "+229") is False
        assert validate_phone("1197123456", "+229") is False

    def test_italian_fixed_lines_keep_their_0(self):
        assert validate_phone("0612345678", "+39") is True
        assert validate_phone("03311234567", "+39") is True
        assert validate_phone("3123456789", "+39") is True
        assert validate_phone("3123456", "+39") is False

    def test_phone_patterns_all_compiled(self):
        import re

        for code, pattern in PHONE_PATTERNS.items():
            assert isinstance(pattern, re.Pattern), f"Pattern for {code} is not compiled"
            assert pattern.flags & re.ASCII, f"Pattern for {code} accepts non-ASCII digits"

    def test_the_whole_number_must_match(self):
        assert validate_phone("7123456789\n", "+44") is False
        assert validate_phone("7123456789 ", "+44") is False
        assert validate_phone("71234567890", "+44") is False

    def test_non_ascii_digits_are_rejected(self):
        fullwidth = "７１２３４５６７８９"
        arabic_indic = "٧١٢٣٤٥٦٧٨٩"
        assert validate_phone(fullwidth, "+44") is False
        assert validate_phone(arabic_indic, "+44") is False

    def test_fallback_rejects_non_ascii_digits(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        arabic_indic = "٠٧١٢٣٤٥٦٧٨٩"
        assert validate_phone_number(arabic_indic, "United Kingdom") is False
        assert validate_phone_number("07123 456789\n", "United Kingdom") is True


class TestFallbackTrunkPrefixes:
    """Without phonenumbers, the fallback drops only the country's own trunk prefix."""

    @pytest.fixture(autouse=True)
    def _without_phonenumbers(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)

    @pytest.mark.parametrize(
        ("number", "jurisdiction"),
        [
            # No trunk prefix: a leading 0 is part of the number.
            ("+225 07 12 34 56 78", "Cote d'Ivoire"),
            ("+2250512345678", "Cote d'Ivoire"),
            ("01 23 45 67 89", "Ivory Coast"),
            ("+229 01 97 12 34 56", "Benin"),
            ("01 97 12 34 56", "Benin"),
            ("+242 06 123 4567", "Congo (Congo-Brazzaville)"),
            ("+226 01 23 45 67", "Burkina Faso"),
            ("+39 06 1234 5678", "Italy"),
            ("+39 0331 1234567", "Italy"),
            ("+241 06 03 12 34", "Gabon"),
            # The trunk prefix is dropped, whatever its digits.
            ("020 7946 0958", "United Kingdom"),
            ("+44 (0)20 7946 0958", "United Kingdom"),
            ("1 (650) 253-0000", "United States"),
            ("8 (912) 345-67-89", "Russia"),
            ("8 (7172) 12 34 56", "Kazakhstan"),
            ("06 1 234 5678", "Hungary"),
            ("06 30 123 4567", "Hungary"),
            ("+36 1 234 5678", "Hungary"),
            ("8 029 123 45 67", "Belarus"),
            ("029 123 45 67", "Belarus"),
            ("8 612 34567", "Lithuania"),
            ("0 612 34567", "Lithuania"),
            # An 8 that starts the number itself stays.
            ("+7 812 123-45-67", "Russia"),
            ("8 800 555 35 35", "Russia"),
        ],
    )
    def test_accepts(self, number, jurisdiction):
        assert validate_phone_number(number, jurisdiction) is True

    @pytest.mark.parametrize(
        ("number", "jurisdiction"),
        [
            ("+229 97 12 34 56", "Benin"),  # 8-digit numbers ended on 2024-11-30
            ("0612345678", "Spain"),  # Spain has no trunk prefix
            ("012345678", "France"),  # the trunk 0 is not one of the nine digits
            ("071234567", "United Kingdom"),  # UK numbers have 9 or 10 digits
            ("02 1234 5678", "United States"),
            ("253-0000", "United States"),  # a local number without its area code
        ],
    )
    def test_rejects(self, number, jurisdiction):
        assert validate_phone_number(number, jurisdiction) is False


class TestLibphonenumberLengths:
    """
    The fallback patterns allow the lengths libphonenumber gives each dial code.

    tests/phone_examples.json freezes libphonenumber 9.0.43's data, so these tests
    give the same answer whichever phonenumbers version is installed, if any.
    """

    # Gabon and San Marino keep lengths they allowed before; libphonenumber has fewer.
    WIDER_THAN_LIBPHONENUMBER = {"+241", "+378"}

    @staticmethod
    def _data() -> dict:
        import json
        from pathlib import Path

        return json.loads(Path(__file__).with_name("phone_examples.json").read_text("utf-8"))

    def test_the_data_covers_every_dial_code(self):
        data = self._data()
        assert sorted(data["lengths"]) == sorted(PHONE_PATTERNS)
        assert sorted(data["national_numbers"]) == sorted(PHONE_PATTERNS)

    def test_patterns_allow_the_libphonenumber_lengths_and_no_others(self):
        for code, lengths in self._data()["lengths"].items():
            pattern = PHONE_PATTERNS[code]
            starts_with_0 = [n for n in range(2, 21) if pattern.fullmatch("01" + "5" * (n - 2))]
            other = [n for n in range(1, 21) if pattern.fullmatch("5" * n)]
            if code in self.WIDER_THAN_LIBPHONENUMBER:
                assert set(lengths["starts_with_0"]) <= set(starts_with_0), code
                assert set(lengths["other"]) <= set(other), code
            else:
                assert starts_with_0 == lengths["starts_with_0"], code
                assert other == lengths["other"], code

    def test_example_national_numbers_validate(self):
        failures = [
            (code, number)
            for code, numbers in self._data()["national_numbers"].items()
            for number in numbers
            if not validate_phone(number, code)
        ]
        assert failures == []

    def test_examples_pass_the_fallback_as_people_write_them(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        failures = [
            (jurisdiction, text)
            for jurisdiction, texts in self._data()["written"].items()
            for text in texts
            if not validate_phone_number(text, jurisdiction)
        ]
        assert failures == []

    @pytest.mark.parametrize(
        ("number", "jurisdiction"),
        [
            ("+49 3012", "Germany"),  # German numbers have 5 to 15 digits
            ("+46 81234", "Sweden"),
            ("+81 3 1234 567", "Japan"),
            ("+245 95 501 234", "Guinea-Bissau"),
            ("+856 20 2312 34567", "Laos"),
            ("+377 6 12 34 56 789", "Monaco"),
            ("+676 771 51234", "Tonga"),
        ],
    )
    def test_wrong_lengths_still_fail(self, monkeypatch, number, jurisdiction):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert validate_phone_number(number, jurisdiction) is False

    @pytest.mark.parametrize(
        ("number", "dial_code"),
        [
            ("30123456", "+49"),  # Berlin fixed line
            ("8123456", "+46"),  # Stockholm fixed line
            ("312345678", "+81"),  # Tokyo fixed line
            ("955012345", "+245"),  # Guinea-Bissau mobile
            ("2023123456", "+856"),  # Laos mobile
            ("770123456", "+231"),  # Liberia mobile
            ("612345678", "+377"),  # Monaco mobile
            ("7715123", "+676"),  # Tonga mobile
            ("8001234567890", "+49"),  # German toll-free
        ],
    )
    def test_real_numbers_of_other_lengths(self, number, dial_code):
        assert validate_phone(number, dial_code) is True

    @pytest.mark.parametrize(
        ("number", "jurisdiction"),
        [
            ("+501 0800 123 4123", "Belize"),
            ("0800 012 345", "Botswana"),
            ("02000", "Norway"),
            ("+227 08 12 34 56", "Niger"),
            ("0800 222", "Tonga"),
        ],
    )
    def test_a_leading_0_stays_where_there_is_no_trunk_prefix(
        self, monkeypatch, number, jurisdiction
    ):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert validate_phone_number(number, jurisdiction) is True

    def test_local_only_lengths_stay_out(self):
        # A length that libphonenumber only knows for local numbers dialled without the
        # area code stays out, even where a rare number type uses it (Canada's 310-1234).
        assert validate_phone("2530000", "+1") is False
        assert validate_phone("3101234", "+1") is False
        assert validate_phone("9460958", "+44") is False


class TestPhoneNumbersExtra:
    def test_phone_extra_available_returns_bool(self):
        assert isinstance(is_phone_extra_available(), bool)

    def test_fallback_validation_without_phonenumbers(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert validate_phone_number("07123456789", "United Kingdom") is True
        assert validate_phone_number("123", "United Kingdom") is False

    def test_formatting_returns_none_without_phonenumbers(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert format_phone_number("07123456789", "United Kingdom") is None
        assert get_phone_number_type("07123456789", "United Kingdom") is None

    def test_phonenumbers_formatting_when_installed(self):
        import pytest

        pytest.importorskip("phonenumbers")

        assert validate_phone_number("6502530000", "United States") is True
        assert format_phone_number("6502530000", "United States") == "+16502530000"
        assert (
            format_phone_number("6502530000", "United States", phone_format="INTERNATIONAL")
            == "+1 650-253-0000"
        )
        assert get_phone_number_type("6502530000", "United States") in {
            "fixed_line",
            "fixed_line_or_mobile",
        }
