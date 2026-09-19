# venv setup notes (uv)

## Create a new project
```
uv init my-project
cd my-project
```
Creates `pyproject.toml`, `.python-version`, and a starter `main.py`.

## Add dependencies
```
uv add numpy pandas
uv add --dev pytest mypy
```
`uv add` resolves versions, writes them to `pyproject.toml`, and updates `uv.lock`.

## Run code without manually activating the venv
```
uv run python main.py
uv run pytest
```
`uv run` creates/reuses `.venv` automatically and runs the command inside it.

## Sync an existing project (e.g. after cloning)
```
uv sync
```
Installs exact versions pinned in `uv.lock`.

## Activate the venv manually (rarely needed with `uv run`)
```
source .venv/bin/activate
```

## Gotcha
`uv.lock` should be committed; `.venv/` should not.
