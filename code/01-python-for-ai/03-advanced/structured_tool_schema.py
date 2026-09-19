from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, field_validator


class WebSearchCall(BaseModel):
    tool: Literal["web_search"] = "web_search"
    query: str = Field(min_length=1, max_length=500)
    max_results: int = Field(default=5, ge=1, le=20)

    @field_validator("query")
    @classmethod
    def query_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query must not be blank; the model should provide search terms")
        return value


class CodeExecutionCall(BaseModel):
    tool: Literal["code_execution"] = "code_execution"
    language: Literal["python", "javascript", "bash"]
    code: str = Field(min_length=1)

    @field_validator("code")
    @classmethod
    def code_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("code must not be blank; provide a runnable snippet")
        return value


class DatabaseQueryCall(BaseModel):
    tool: Literal["database_query"] = "database_query"
    table: str
    filters: dict[str, str | int | float] = Field(default_factory=dict)
    limit: int = Field(default=100, ge=1, le=1000)

    @field_validator("table")
    @classmethod
    def table_name_valid(cls, value: str) -> str:
        if not value.isidentifier():
            raise ValueError(f"'{value}' is not a valid table name; use a plain identifier")
        return value


ToolCall = Annotated[
    Union[WebSearchCall, CodeExecutionCall, DatabaseQueryCall],
    Field(discriminator="tool"),
]


class ToolCallEnvelope(BaseModel):
    call: ToolCall


if __name__ == "__main__":
    examples = [
        {"call": {"tool": "web_search", "query": "latest LLM benchmarks"}},
        {"call": {"tool": "code_execution", "language": "python", "code": "print(1 + 1)"}},
        {"call": {"tool": "database_query", "table": "users", "filters": {"active": 1}}},
    ]
    for example in examples:
        envelope = ToolCallEnvelope.model_validate(example)
        print(envelope.call)
