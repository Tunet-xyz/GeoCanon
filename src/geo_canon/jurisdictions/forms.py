"""
Django form fields and forms for jurisdiction context-switching.
"""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from . import get_jurisdiction_choices


class JurisdictionChoiceField(forms.ChoiceField):
    """
    A ``ChoiceField`` pre-populated with all GeoCanon jurisdictions.

    Usable standalone in any Django form::

        class MyForm(forms.Form):
            country = JurisdictionChoiceField()
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _("Jurisdiction"))
        kwargs.setdefault("choices", get_jurisdiction_choices)
        super().__init__(**kwargs)


class JurisdictionContextSwitchForm(forms.Form):
    """
    A drop-in Django form that lets users switch their active jurisdiction.

    Usage in a view::

        form = JurisdictionContextSwitchForm(request.POST or None)
        if form.is_valid():
            request.session["jurisdiction"] = form.cleaned_data["jurisdiction"]
    """

    jurisdiction = JurisdictionChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}),
    )
