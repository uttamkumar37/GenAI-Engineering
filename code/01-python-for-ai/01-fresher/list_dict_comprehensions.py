from __future__ import annotations


def flatten(nested: list[list[int]]) -> list[int]:
    return [item for row in nested for item in row]


def filter_even(numbers: list[int]) -> list[int]:
    return [n for n in numbers if n % 2 == 0]


def square_map(numbers: list[int]) -> dict[int, int]:
    return {n: n * n for n in numbers}


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    groups: dict[int, list[str]] = {}
    for word in words:
        groups.setdefault(len(word), []).append(word)
    return groups


def invert_dict(mapping: dict[str, int]) -> dict[int, str]:
    return {value: key for key, value in mapping.items()}


def unique_sorted(numbers: list[int]) -> list[int]:
    return sorted({n for n in numbers})


def zip_to_dict(keys: list[str], values: list[int]) -> dict[str, int]:
    return {key: value for key, value in zip(keys, values)}


if __name__ == "__main__":
    print(flatten([[1, 2], [3, 4], [5]]))
    print(filter_even([1, 2, 3, 4, 5, 6]))
    print(square_map([1, 2, 3]))
    print(group_by_length(["a", "bb", "cc", "ddd"]))
    print(invert_dict({"a": 1, "b": 2}))
    print(unique_sorted([3, 1, 2, 1, 3]))
    print(zip_to_dict(["a", "b"], [1, 2]))
