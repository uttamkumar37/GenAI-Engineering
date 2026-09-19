from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from structured_tool_schema import ToolCallEnvelope


@given(query=st.text(min_size=1, max_size=500).filter(lambda s: s.strip() != ""))
def test_web_search_accepts_any_nonblank_query(query: str) -> None:
    envelope = ToolCallEnvelope.model_validate({"call": {"tool": "web_search", "query": query}})
    assert envelope.call.query == query


@given(query=st.just(""))
def test_web_search_rejects_blank_query(query: str) -> None:
    with pytest.raises(ValidationError):
        ToolCallEnvelope.model_validate({"call": {"tool": "web_search", "query": query}})


@given(max_results=st.integers(min_value=1, max_value=20))
def test_web_search_max_results_in_bounds_accepted(max_results: int) -> None:
    envelope = ToolCallEnvelope.model_validate(
        {"call": {"tool": "web_search", "query": "x", "max_results": max_results}}
    )
    assert envelope.call.max_results == max_results


@given(max_results=st.integers(max_value=0))
def test_web_search_max_results_below_bound_rejected(max_results: int) -> None:
    with pytest.raises(ValidationError):
        ToolCallEnvelope.model_validate(
            {"call": {"tool": "web_search", "query": "x", "max_results": max_results}}
        )


@given(table=st.text(alphabet=st.characters(whitelist_categories=("Nd",)), min_size=1, max_size=5))
def test_database_query_rejects_numeric_table_names(table: str) -> None:
    with pytest.raises(ValidationError):
        ToolCallEnvelope.model_validate({"call": {"tool": "database_query", "table": table}})
