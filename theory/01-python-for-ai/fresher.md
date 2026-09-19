# 01 — Python for AI — Fresher

**Concepts**: variables/types recap, functions, list/dict comprehensions, `*args`/`**kwargs`, virtual environments, type hints basics (`str`, `int`, `list[str]`, `Optional`).

**Resources**:
- [Python typing docs — typing module basics](https://docs.python.org/3/library/typing.html) (skim intro + common types)
- [Real Python — Python Type Checking Guide](https://realpython.com/python-type-checking/) (intro section only)

**Code** (`code/01-python-for-ai/01-fresher/`):
- `type_hints_basics.py` — functions with full type annotations, run through `mypy`
- `list_dict_comprehensions.py` — data transformation drills (flatten, filter, group)
- `venv_setup.md` — notes on `uv init`, `uv add`, `uv run`

**Interview questions**:
- What's the difference between `list` and `List[str]` in type hints, and does Python enforce them at runtime? (No — hints are documentation + static-analysis only, unless you validate explicitly, which is exactly why Pydantic exists.)
