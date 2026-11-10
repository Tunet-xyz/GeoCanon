"""Tests for geo_canon.currencies"""

from decimal import Decimal

from geo_canon.currencies import (
    _WITHDRAWN_CURRENCIES,
    CURRENCY_BY_CODE,
    CURRENCY_CHOICES,
    JURISDICTION_CURRENCY,
    CurrencyInfo,
    format_currency,
    get_currency_by_code,
    get_currency_choices,
    get_currency_code,
    get_currency_for_jurisdiction,
    get_currency_symbol,
)


class TestCurrencyRegistry:
    def test_jurisdiction_currency_not_empty(self):
        assert len(JURISDICTION_CURRENCY) > 150

    def test_currency_by_code_not_empty(self):
        assert len(CURRENCY_BY_CODE) > 50

    def test_currency_choices_not_empty(self):
        assert len(CURRENCY_CHOICES) > 50

    def test_currency_choices_are_tuples(self):
        assert all(isinstance(c, tuple) and len(c) == 2 for c in CURRENCY_CHOICES)

    def test_currency_choices_sorted(self):
        labels = [str(c[1]) for c in CURRENCY_CHOICES]
        assert labels == sorted(labels)

    def test_currency_info_is_named_tuple(self):
        info = JURISDICTION_CURRENCY["Romania"]
        assert isinstance(info, CurrencyInfo)
        assert info.code == "RON"
        assert info.symbol == "lei"
        assert info.decimal_places == 2


class TestGetCurrencyForJurisdiction:
    def test_romania(self):
        info = get_currency_for_jurisdiction("Romania")
        assert info is not None
        assert info.code == "RON"
        assert info.symbol == "lei"

    def test_united_kingdom(self):
        info = get_currency_for_jurisdiction("United Kingdom")
        assert info is not None
        assert info.code == "GBP"
        assert info.symbol == "£"

    def test_united_states(self):
        info = get_currency_for_jurisdiction("United States")
        assert info is not None
        assert info.code == "USD"
        assert info.symbol == "$"

    def test_japan(self):
        info = get_currency_for_jurisdiction("Japan")
        assert info is not None
        assert info.code == "JPY"
        assert info.decimal_places == 0

    def test_eurozone_country(self):
        info = get_currency_for_jurisdiction("Germany")
        assert info is not None
        assert info.code == "EUR"
        assert info.symbol == "€"

    def test_unknown_returns_none(self):
        assert get_currency_for_jurisdiction("Narnia") is None

    def test_bahrain_3_decimal_places(self):
        info = get_currency_for_jurisdiction("Bahrain")
        assert info is not None
        assert info.code == "BHD"
        assert info.decimal_places == 3


class TestGetCurrencyCode:
    def test_returns_code(self):
        assert get_currency_code("Romania") == "RON"

    def test_unknown_returns_none(self):
        assert get_currency_code("Narnia") is None


class TestGetCurrencySymbol:
    def test_returns_symbol(self):
        assert get_currency_symbol("United Kingdom") == "£"

    def test_unknown_returns_none(self):
        assert get_currency_symbol("Narnia") is None


class TestGetCurrencyByCode:
    def test_eur(self):
        info = get_currency_by_code("EUR")
        assert info is not None
        assert info.symbol == "€"

    def test_lowercase(self):
        info = get_currency_by_code("eur")
        assert info is not None
        assert info.code == "EUR"

    def test_unknown_returns_none(self):
        assert get_currency_by_code("XYZ") is None


class TestGetCurrencyChoices:
    def test_returns_list(self):
        choices = get_currency_choices()
        assert isinstance(choices, list)
        assert len(choices) > 50

    def test_each_has_code_and_label(self):
        choices = get_currency_choices()
        for code, _label in choices:
            assert isinstance(code, str)
            assert len(code) == 3  # ISO 4217


class TestFormatCurrency:
    def test_gbp(self):
        assert format_currency(1234.50, "United Kingdom") == "£1,234.50"

    def test_usd(self):
        assert format_currency(99.99, "United States") == "$99.99"

    def test_jpy_zero_decimals(self):
        assert format_currency(1234.5, "Japan") == "¥1,235"

    def test_eur(self):
        assert format_currency(42, "Germany") == "€42.00"

    def test_bhd_three_decimals(self):
        assert format_currency(100, "Bahrain") == ".د.ب100.000"

    def test_ron(self):
        assert format_currency(49.99, "Romania") == "lei49.99"

    def test_large_number_has_thousands_separator(self):
        result = format_currency(1234567.89, "United States")
        assert result == "$1,234,567.89"

    def test_code_only(self):
        result = format_currency(49.99, "Romania", use_symbol=False, include_code=True)
        assert result == "49.99 RON"

    def test_symbol_and_code(self):
        result = format_currency(100, "United Kingdom", use_symbol=True, include_code=True)
        assert result == "£100.00 GBP"

    def test_no_symbol_no_code(self):
        result = format_currency(100, "United Kingdom", use_symbol=False, include_code=False)
        assert result == "100.00"

    def test_unknown_jurisdiction_fallback(self):
        result = format_currency(100, "Narnia")
        assert result == "100.00"

    def test_decimal_input(self):
        result = format_currency(Decimal("99.999"), "United States")
        assert result == "$100.00"


class TestReplacedCurrencies:
    """Bulgaria, Zimbabwe and Curacao replaced their currencies in 2024-2026."""

    def test_bulgaria_uses_the_euro(self):
        assert get_currency_for_jurisdiction("Bulgaria") == get_currency_for_jurisdiction("Germany")
        assert format_currency(1234.5, "Bulgaria") == "€1,234.50"

    def test_zimbabwe_uses_zimbabwe_gold(self):
        info = get_currency_for_jurisdiction("Zimbabwe")
        assert info is not None
        assert (info.code, info.symbol, info.decimal_places) == ("ZWG", "ZiG", 2)
        assert str(info.name) == "Zimbabwe Gold"

    def test_curacao_uses_the_caribbean_guilder(self):
        info = get_currency_for_jurisdiction("Curacao")
        assert info is not None
        assert (info.code, info.symbol, info.decimal_places) == ("XCG", "Cg", 2)
        assert str(info.name) == "Caribbean Guilder"

    def test_no_jurisdiction_uses_a_withdrawn_currency(self):
        in_use = {info.code for info in JURISDICTION_CURRENCY.values()}
        assert sorted(in_use & set(_WITHDRAWN_CURRENCIES)) == []

    def test_withdrawn_codes_still_resolve_for_stored_amounts(self):
        for code in ("BGN", "ZWL", "ANG"):
            assert get_currency_by_code(code) == _WITHDRAWN_CURRENCIES[code]
            assert get_currency_by_code(code.lower()) == _WITHDRAWN_CURRENCIES[code]
        assert get_currency_by_code("BGN").symbol == "лв"

    def test_choices_offer_only_currencies_in_use(self):
        choice_codes = {code for code, _label in CURRENCY_CHOICES}
        assert {"EUR", "ZWG", "XCG"} <= choice_codes
        assert sorted(choice_codes & set(_WITHDRAWN_CURRENCIES)) == []
        assert choice_codes == {info.code for info in JURISDICTION_CURRENCY.values()}
