from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class ReplayExchange:
    request: bytes
    response: bytes
    timestamp: str | None = None
    transport: str = "unknown"
    protocol: str = "unknown"
    source: str = "fixture"

    @property
    def digest(self) -> str:
        body = {
            "request": self.request.hex(),
            "response": self.response.hex(),
            "timestamp": self.timestamp,
            "transport": self.transport,
            "protocol": self.protocol,
            "source": self.source,
        }
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        return sha256(canonical).hexdigest()


class ReplayExchangeEngine:
    def __init__(self, exchanges: list[ReplayExchange]):
        self._exchanges = list(exchanges)
        self._index = 0

    def request(self, payload: bytes) -> bytes:
        if self._index >= len(self._exchanges):
            raise LookupError("replay exhausted")
        exchange = self._exchanges[self._index]
        if exchange.request != payload:
            raise ValueError(
                f"replay mismatch at index {self._index}: "
                f"expected {exchange.request.hex()}, got {payload.hex()}"
            )
        self._index += 1
        return exchange.response

    @property
    def consumed(self) -> int:
        return self._index

    @property
    def remaining(self) -> int:
        return len(self._exchanges) - self._index
