# requires ANTHROPIC_API_KEY for the real client; FakeExtractionClient needs nothing
from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any

INVOICE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string"},
        "vendor": {"type": "string"},
        "total_amount": {"type": "number"},
        "currency": {"type": "string"},
        "due_date": {"type": "string"},
    },
    "required": ["invoice_number", "vendor", "total_amount", "currency", "due_date"],
    "additionalProperties": False,
}

SAMPLE_INVOICE_TEXT = """
Invoice #INV-2024-0917 from Acme Cloud Services.
Total due: $1,284.50 USD, payable by 2026-10-15.
"""


class ExtractionClient(ABC):
    @abstractmethod
    def extract(self, text: str, schema: dict[str, Any]) -> dict[str, Any]: ...


class AnthropicExtractionClient(ExtractionClient):
    def __init__(self, model: str = "claude-opus-5") -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def extract(self, text: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[{"role": "user", "content": f"Extract invoice fields from:\n{text}"}],
            output_config={"format": {"type": "json_schema", "schema": schema}},
        )
        raw = next(b.text for b in response.content if b.type == "text")
        return json.loads(raw)


class FakeExtractionClient(ExtractionClient):
    # deterministic regex-based stand-in so the pipeline is testable offline
    def extract(self, text: str, schema: dict[str, Any]) -> dict[str, Any]:
        invoice_number = re.search(r"#([\w-]+)", text)
        vendor = re.search(r"from ([A-Za-z0-9 ]+?)\.", text)
        amount = re.search(r"\$([\d,]+\.\d{2})", text)
        due_date = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        return {
            "invoice_number": invoice_number.group(1) if invoice_number else "",
            "vendor": vendor.group(1).strip() if vendor else "",
            "total_amount": float(amount.group(1).replace(",", "")) if amount else 0.0,
            "currency": "USD",
            "due_date": due_date.group(1) if due_date else "",
        }


if __name__ == "__main__":
    client: ExtractionClient = (
        AnthropicExtractionClient()
        if os.environ.get("ANTHROPIC_API_KEY")
        else FakeExtractionClient()
    )
    result = client.extract(SAMPLE_INVOICE_TEXT, INVOICE_SCHEMA)
    print(json.dumps(result, indent=2))
