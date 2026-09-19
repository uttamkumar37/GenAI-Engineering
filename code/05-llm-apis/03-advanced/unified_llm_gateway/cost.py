from __future__ import annotations

# USD per 1M tokens: (input, output). Update as pricing changes.
PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "llama3.2": (0.0, 0.0),
}

CACHE_READ_DISCOUNT = 0.1  # cached input tokens cost ~10% of standard input price


def estimate_cost(
    model: str, input_tokens: int, output_tokens: int, cache_read_tokens: int = 0
) -> float:
    input_price, output_price = PRICING.get(model, (0.0, 0.0))
    standard_input = max(input_tokens - cache_read_tokens, 0)
    cost = (
        standard_input * input_price
        + cache_read_tokens * input_price * CACHE_READ_DISCOUNT
        + output_tokens * output_price
    ) / 1_000_000
    return round(cost, 8)
