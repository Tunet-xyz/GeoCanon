"""Tests for geo_canon.address_formats."""

from geo_canon.address_formats import (
    JURISDICTION_ADDRESS_FORMAT,
    AddressFormat,
    format_address,
    get_address_format,
    get_postal_code_label,
    get_postal_code_regex,
    get_state_label,
    is_state_required,
    validate_postal_code,
)

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestAddressFormatRegistry:
    """Sanity checks on the master registry."""

    def test_registry_not_empty(self):
        assert len(JURISDICTION_ADDRESS_FORMAT) > 100

    def test_values_are_address_format(self):
        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            assert isinstance(v, AddressFormat), f"{k} is not AddressFormat"

    def test_all_have_template(self):
        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            assert v.template, f"{k} has empty template"

    def test_all_have_state_label(self):
        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            assert v.state_label, f"{k} has empty state_label"

    def test_all_have_postal_code_label(self):
        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            assert v.postal_code_label, f"{k} has empty postal_code_label"

    def test_state_required_is_bool(self):
        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            assert isinstance(v.state_required, bool), f"{k} state_required not bool"

    def test_example_consistent_with_pattern(self):
        """If a jurisdiction has a postal code pattern, the example should match it."""
        import re

        for k, v in JURISDICTION_ADDRESS_FORMAT.items():
            if v.postal_code_pattern and v.postal_code_example:
                assert re.match(v.postal_code_pattern, v.postal_code_example, re.IGNORECASE), (
                    f"{k}: example '{v.postal_code_example}' "
                    f"doesn't match pattern '{v.postal_code_pattern}'"
                )


# ---------------------------------------------------------------------------
# get_address_format
# ---------------------------------------------------------------------------


class TestGetAddressFormat:
    def test_united_states(self):
        fmt = get_address_format("United States")
        assert fmt is not None
        assert str(fmt.state_label) == "State"
        assert str(fmt.postal_code_label) == "ZIP Code"
        assert fmt.state_required is True

    def test_united_kingdom(self):
        fmt = get_address_format("United Kingdom")
        assert fmt is not None
        assert str(fmt.state_label) == "County"
        assert str(fmt.postal_code_label) == "Postcode"
        assert fmt.state_required is False

    def test_japan(self):
        fmt = get_address_format("Japan")
        assert fmt is not None
        assert str(fmt.state_label) == "Prefecture"
        assert fmt.state_required is True

    def test_germany(self):
        fmt = get_address_format("Germany")
        assert fmt is not None
        assert str(fmt.postal_code_label) == "PLZ"

    def test_brazil(self):
        fmt = get_address_format("Brazil")
        assert fmt is not None
        assert str(fmt.postal_code_label) == "CEP"
        assert fmt.state_required is True

    def test_romania(self):
        fmt = get_address_format("Romania")
        assert fmt is not None
        assert str(fmt.state_label) == "County"
        assert str(fmt.postal_code_label) == "Cod Poștal"

    def test_unknown_returns_none(self):
        assert get_address_format("Narnia") is None


# ---------------------------------------------------------------------------
# validate_postal_code
# ---------------------------------------------------------------------------


class TestValidatePostalCode:
    def test_us_valid(self):
        assert validate_postal_code("United States", "10001") is True

    def test_us_zip_plus_4(self):
        assert validate_postal_code("United States", "10001-1234") is True

    def test_us_invalid(self):
        assert validate_postal_code("United States", "ABCDE") is False

    def test_uk_valid(self):
        assert validate_postal_code("United Kingdom", "SW1A 1AA") is True

    def test_uk_no_space(self):
        assert validate_postal_code("United Kingdom", "SW1A1AA") is True

    def test_uk_invalid(self):
        assert validate_postal_code("United Kingdom", "12345") is False

    def test_canada_valid(self):
        assert validate_postal_code("Canada", "K1A 0B1") is True

    def test_canada_no_space(self):
        assert validate_postal_code("Canada", "K1A0B1") is True

    def test_japan_valid(self):
        assert validate_postal_code("Japan", "100-0001") is True

    def test_japan_no_dash(self):
        assert validate_postal_code("Japan", "1000001") is True

    def test_germany_valid(self):
        assert validate_postal_code("Germany", "10115") is True

    def test_germany_invalid(self):
        assert validate_postal_code("Germany", "1011") is False

    def test_brazil_valid(self):
        assert validate_postal_code("Brazil", "01001-000") is True

    def test_brazil_no_dash(self):
        assert validate_postal_code("Brazil", "01001000") is True

    def test_netherlands_valid(self):
        assert validate_postal_code("Netherlands", "1011 AB") is True

    def test_india_valid(self):
        assert validate_postal_code("India", "110001") is True

    def test_no_postal_system_accepts_anything(self):
        """Hong Kong, Angola etc. have no postal code — always valid."""
        assert validate_postal_code("Hong Kong", "") is True
        assert validate_postal_code("Angola", "anything") is True

    def test_unknown_jurisdiction_returns_false(self):
        assert validate_postal_code("Narnia", "12345") is False

    def test_romania_valid(self):
        assert validate_postal_code("Romania", "010011") is True

    def test_romania_invalid(self):
        assert validate_postal_code("Romania", "1234") is False

    def test_australia_valid(self):
        assert validate_postal_code("Australia", "2000") is True

    def test_france_valid(self):
        assert validate_postal_code("France", "75001") is True

    def test_poland_valid(self):
        assert validate_postal_code("Poland", "00-001") is True

    def test_switzerland_valid(self):
        assert validate_postal_code("Switzerland", "3000") is True

    def test_strips_whitespace(self):
        assert validate_postal_code("United States", " 10001 ") is True
        assert validate_postal_code("United States", "\t10001\n") is True

    def test_letters_match_case_insensitively(self):
        assert validate_postal_code("Canada", "k1a 0b1") is True

    def test_non_ascii_lookalikes_are_rejected(self):
        # Fullwidth and Arabic-Indic digits, the Kelvin sign that case-folds to "k",
        # and no-break spaces inside or around the code.
        assert validate_postal_code("United States", "１０００１") is False
        assert validate_postal_code("United States", "١٠٠٠١") is False
        assert validate_postal_code("Canada", "K1A 0B1") is False
        assert validate_postal_code("Canada", "K1A 0B1") is False
        assert validate_postal_code("United States", " 10001 ") is False

    def test_the_whole_code_must_match(self):
        assert validate_postal_code("United States", "10001 trailing") is False
        assert validate_postal_code("United States", "10001\nX") is False


# ---------------------------------------------------------------------------
# get_state_label / get_postal_code_label
# ---------------------------------------------------------------------------


class TestLabels:
    def test_state_label_us(self):
        assert get_state_label("United States") == "State"

    def test_state_label_japan(self):
        assert get_state_label("Japan") == "Prefecture"

    def test_state_label_canada(self):
        assert get_state_label("Canada") == "Province"

    def test_state_label_ireland(self):
        assert get_state_label("Ireland") == "County"

    def test_state_label_uae(self):
        assert get_state_label("United Arab Emirates") == "Emirate"

    def test_state_label_unknown(self):
        assert get_state_label("Narnia") is None

    def test_postal_code_label_us(self):
        assert get_postal_code_label("United States") == "ZIP Code"

    def test_postal_code_label_uk(self):
        assert get_postal_code_label("United Kingdom") == "Postcode"

    def test_postal_code_label_germany(self):
        assert get_postal_code_label("Germany") == "PLZ"

    def test_postal_code_label_france(self):
        assert get_postal_code_label("France") == "Code Postal"

    def test_postal_code_label_brazil(self):
        assert get_postal_code_label("Brazil") == "CEP"

    def test_postal_code_label_india(self):
        assert get_postal_code_label("India") == "PIN Code"

    def test_postal_code_label_unknown(self):
        assert get_postal_code_label("Narnia") is None


# ---------------------------------------------------------------------------
# is_state_required
# ---------------------------------------------------------------------------


class TestIsStateRequired:
    def test_us_required(self):
        assert is_state_required("United States") is True

    def test_australia_required(self):
        assert is_state_required("Australia") is True

    def test_brazil_required(self):
        assert is_state_required("Brazil") is True

    def test_france_not_required(self):
        assert is_state_required("France") is False

    def test_uk_not_required(self):
        assert is_state_required("United Kingdom") is False

    def test_unknown_returns_false(self):
        assert is_state_required("Narnia") is False


# ---------------------------------------------------------------------------
# format_address
# ---------------------------------------------------------------------------


class TestFormatAddress:
    def test_us_format(self):
        result = format_address(
            "United States",
            address1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="United States",
        )
        assert "123 Main St" in result
        assert "New York, NY 10001" in result
        assert "United States" in result

    def test_uk_format(self):
        result = format_address(
            "United Kingdom",
            address1="10 Downing Street",
            city="London",
            postal_code="SW1A 2AA",
            country="United Kingdom",
        )
        assert "10 Downing Street" in result
        assert "London" in result
        assert "SW1A 2AA" in result

    def test_germany_format(self):
        result = format_address(
            "Germany",
            address1="Unter den Linden 1",
            city="Berlin",
            postal_code="10117",
            country="Germany",
        )
        lines = result.splitlines()
        # PLZ before city in German format
        assert any("10117" in line and "Berlin" in line for line in lines)

    def test_japan_reversed_format(self):
        result = format_address(
            "Japan",
            address1="1-1 Chiyoda",
            state="Tokyo",
            city="Chiyoda-ku",
            postal_code="100-0001",
        )
        lines = result.splitlines()
        # Postal code should appear before address in JP format
        assert "100-0001" in lines[0]

    def test_blank_lines_collapsed(self):
        """Empty fields should not produce blank lines."""
        result = format_address(
            "United States",
            address1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
        )
        for line in result.splitlines():
            assert line.strip(), "Blank line found in formatted address"

    def test_unknown_jurisdiction_fallback(self):
        result = format_address(
            "Narnia",
            name="Mr. Tumnus",
            address1="Lamp Post Lane",
            city="Cair Paravel",
        )
        assert "Mr. Tumnus" in result
        assert "Lamp Post Lane" in result
        assert "Cair Paravel" in result

    def test_singapore_format(self):
        result = format_address(
            "Singapore",
            address1="1 Raffles Place",
            postal_code="048616",
        )
        assert "Singapore 048616" in result

    def test_recipient_comes_first_in_small_to_large_orders(self):
        result = format_address(
            "United States",
            name="Jane Doe",
            company="Acme Inc.",
            address1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="United States",
        )
        assert result.splitlines() == [
            "Jane Doe",
            "Acme Inc.",
            "123 Main St",
            "New York, NY 10001",
            "United States",
        ]

    def test_recipient_comes_last_in_large_to_small_orders(self):
        result = format_address(
            "Japan",
            name="Taro Yamada",
            company="Example KK",
            address1="1-1 Chiyoda",
            state="Tokyo",
            city="Chiyoda-ku",
            postal_code="100-0001",
        )
        assert result.splitlines()[-2:] == ["Example KK", "Taro Yamada"]

    def test_china_shows_the_postal_code(self):
        result = format_address(
            "China",
            address1="1 Chang'an Avenue",
            city="Dongcheng",
            state="Beijing",
            postal_code="100000",
            country="China",
        )
        assert result.splitlines()[:3] == ["China", "100000", "Beijing"]

    def test_required_state_is_shown(self):
        spain = format_address(
            "Spain", address1="Calle Mayor 1", city="Madrid", state="Madrid", postal_code="28001"
        )
        assert "28001 Madrid Madrid" in spain.splitlines()
        nigeria = format_address(
            "Nigeria", address1="1 Marina", city="Lagos Island", state="Lagos", postal_code="101001"
        )
        assert nigeria.splitlines()[-1] == "Lagos"

    def test_empty_fields_leave_no_stray_spaces(self):
        spain = format_address("Spain", address1="Calle Mayor 1", city="Madrid", postal_code="28001")
        assert spain.splitlines() == ["Calle Mayor 1", "28001 Madrid"]
        canada = format_address("Canada", address1="1 Main St", city="Toronto", postal_code="M5V 2T6")
        assert canada.splitlines() == ["1 Main St", "Toronto M5V 2T6"]


class TestTemplatesUseTheirFields:
    def test_every_template_places_the_recipient(self):
        for name, fmt in JURISDICTION_ADDRESS_FORMAT.items():
            assert "{name}" in fmt.template, name
            assert "{company}" in fmt.template, name

    def test_required_states_appear_in_the_template(self):
        for name, fmt in JURISDICTION_ADDRESS_FORMAT.items():
            if fmt.state_required:
                assert "{state}" in fmt.template, name

    def test_postal_codes_with_a_pattern_appear_in_the_template(self):
        for name, fmt in JURISDICTION_ADDRESS_FORMAT.items():
            if fmt.postal_code_pattern:
                assert "{postal_code}" in fmt.template, name


# ---------------------------------------------------------------------------
# get_postal_code_regex
# ---------------------------------------------------------------------------


class TestGetPostalCodeRegex:
    def test_returns_pattern_for_known(self):
        pattern = get_postal_code_regex("United States")
        assert pattern is not None
        assert r"\d{5}" in pattern

    def test_returns_empty_for_no_system(self):
        pattern = get_postal_code_regex("Hong Kong")
        assert pattern == ""

    def test_returns_none_for_unknown(self):
        assert get_postal_code_regex("Narnia") is None
