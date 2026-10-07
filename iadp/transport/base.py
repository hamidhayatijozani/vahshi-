from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CanFrame:
    arbitration_id: int
    data: bytes
    is_extended_id: bool = False
    is_fd: bool = False

    def __post_init__(self) -> None:
        if not 0 <= self.arbitration_id <= 0x1FFFFFFF:
            raise ValueError("CAN arbitration ID out of range")
        if len(self.data) > (64 if self.is_fd else 8):
            raise ValueError("CAN payload exceeds selected frame capacity")


class Transport(ABC):
    @abstractmethod
    def send(self, payload: bytes) -> None: ...

    @abstractmethod
    def receive(self, timeout: float = 1.0) -> bytes | None: ...


class CanTransport(ABC):
    @abstractmethod
    def send_frame(self, frame: CanFrame) -> None: ...

    @abstractmethod
    def receive_frame(self, timeout: float = 1.0) -> CanFrame | None: ...


class MemoryCanTransport(CanTransport):
    """Deterministic in-memory CAN transport for protocol and integration tests."""

    def __init__(self) -> None:
        self.sent: list[CanFrame] = []
        self.incoming: list[CanFrame] = []

    def send_frame(self, frame: CanFrame) -> None:
        self.sent.append(frame)

    def receive_frame(self, timeout: float = 1.0) -> CanFrame | None:
        if not self.incoming:
            return None
        return self.incoming.pop(0)

    def queue(self, *frames: CanFrame) -> None:
        self.incoming.extend(frames)
