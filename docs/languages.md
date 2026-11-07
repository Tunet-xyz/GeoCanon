# Languages

Language choices for forms and jurisdiction → language mapping.

## Data

- `LANGUAGE_CHOICES` — 70+ languages as `(code, translatable_name)` tuples
- `JURISDICTION_LANGUAGE` — dict mapping jurisdiction name → ISO 639-1 code

## Functions

### `get_language_choices() -> list[tuple[str, str]]`
Returns `LANGUAGE_CHOICES` for a Django `ChoiceField`.

### `get_language_for_jurisdiction(jurisdiction: str) -> str | None`
```python
get_language_for_jurisdiction("Romania")  # "ro"
get_language_for_jurisdiction("Japan")    # "ja"
```
