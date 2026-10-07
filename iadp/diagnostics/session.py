from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

class Exchange(Protocol):
    def request(self, payload: bytes) -> bytes: ...

@dataclass
class DiagnosticSession:
    exchange: Exchange

    def read_data_by_identifier(self, did: int) -> bytes:
        from iadp.protocols.uds import make_read_data_by_identifier
        return self.exchange.request(make_read_data_by_identifier(did))
