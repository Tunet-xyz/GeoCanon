# Jurisdictions

GeoCanon ships with a canonical list of 190+ jurisdictions (countries and territories).
Keys are ASCII, for example `"Cote d'Ivoire"` (shown as "Côte d'Ivoire"). Every
lookup also accepts the legacy names "Cape Verde", "Congo", "Democratic
Republic of Congo", "Ivory Coast", "North Korea", and "South Korea".

## Data

```python
from geo_canon.jurisdictions import JURISDICTIONS, JURISDICTION_NAMES

# List of (key, translatable_label) tuples
JURISDICTIONS  # [("Afghanistan", "Afghanistan"), ...]

# Set for O(1) lookups
JURISDICTION_NAMES  # {"Afghanistan", "Albania", ...}
```

## Functions

### `get_jurisdiction_choices()`
Returns the full list as Django `ChoiceField` compatible tuples.

### `is_valid_jurisdiction(name: str) -> bool`
O(1) check whether a string is a recognised jurisdiction.

## Forms

```python
from geo_canon.jurisdictions.forms import (
    JurisdictionChoiceField,           # Drop-in ChoiceField
    JurisdictionContextSwitchForm,     # Complete form for nav bars
)
```

## Middleware

Add to `MIDDLEWARE`:

```python
"geo_canon.jurisdictions.middleware.JurisdictionMiddleware"
```

This sets `request.jurisdiction` from `request.session["jurisdiction"]` or falls back to `GEOCANON.default_jurisdiction`.
