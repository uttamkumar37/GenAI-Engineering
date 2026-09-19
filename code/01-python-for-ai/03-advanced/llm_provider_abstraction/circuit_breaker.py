from __future__ import annotations

import time
from enum import Enum, auto


class CircuitState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout_s: float = 5.0) -> None:
        self._failure_threshold = failure_threshold
        self._reset_timeout_s = reset_timeout_s
        self._consecutive_failures = 0
        self._state = CircuitState.CLOSED
        self._opened_at: float | None = None

    @property
    def state(self) -> CircuitState:
        if self._state is CircuitState.OPEN and self._opened_at is not None:
            if time.monotonic() - self._opened_at >= self._reset_timeout_s:
                self._state = CircuitState.HALF_OPEN
        return self._state

    def before_call(self) -> None:
        if self.state is CircuitState.OPEN:
            raise CircuitOpenError("circuit is open, failing fast")

    def record_success(self) -> None:
        self._consecutive_failures = 0
        self._state = CircuitState.CLOSED
        self._opened_at = None

    def record_failure(self) -> None:
        self._consecutive_failures += 1
        if self._consecutive_failures >= self._failure_threshold:
            self._state = CircuitState.OPEN
            self._opened_at = time.monotonic()
