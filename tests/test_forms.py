"""Tests for geo_canon.jurisdictions.forms"""

from geo_canon.jurisdictions.forms import (
    JurisdictionChoiceField,
    JurisdictionContextSwitchForm,
)


class TestJurisdictionForms:
    def test_context_switch_form_valid(self):
        form = JurisdictionContextSwitchForm(data={"jurisdiction": "Romania"})
        assert form.is_valid()

    def test_context_switch_form_invalid(self):
        form = JurisdictionContextSwitchForm(data={"jurisdiction": "Narnia"})
        assert not form.is_valid()

    def test_jurisdiction_choice_field_has_choices(self):
        field = JurisdictionChoiceField()
        choices = list(field.choices)
        assert len(choices) > 100
