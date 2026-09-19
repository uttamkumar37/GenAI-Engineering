from __future__ import annotations

from collections.abc import Callable


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


def total_length(items: list[str]) -> int:
    return sum(len(item) for item in items)


def find_user(user_id: int, users: dict[int, str]) -> str | None:
    return users.get(user_id)


def average(numbers: list[float]) -> float:
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def make_pair(first: int, second: str) -> tuple[int, str]:
    return first, second


def apply_all(value: int, funcs: list[Callable[[int], int]]) -> list[int]:
    return [func(value) for func in funcs]


def merge_counts(*counts: dict[str, int]) -> dict[str, int]:
    merged: dict[str, int] = {}
    for count in counts:
        for key, value in count.items():
            merged[key] = merged.get(key, 0) + value
    return merged


def build_config(**settings: str | int | bool) -> dict[str, str | int | bool]:
    return dict(settings)


if __name__ == "__main__":
    print(add(2, 3))
    print(greet("World"))
    print(total_length(["ai", "genai", "llm"]))
    print(find_user(1, {1: "alice"}))
    print(average([1.0, 2.0, 3.0]))
    print(make_pair(1, "one"))
    print(merge_counts({"a": 1}, {"a": 2, "b": 1}))
    print(build_config(debug=True, retries=3))
