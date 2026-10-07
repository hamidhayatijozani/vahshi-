from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class CanFrame:
    arbitration_id: int
    data: bytes
    is_extended_id: bool = False
    is_fd: bool = False

class Transport(ABC):
    @abstractmethod
    def send(self, payload: bytes) -> None: ...

    @abstractmethod
    def receive(self, timeout: float = 1.0) -> bytes | None: ...
