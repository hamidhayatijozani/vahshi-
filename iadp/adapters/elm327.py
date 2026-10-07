from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Elm327Error(ValueError):
    pass


class LineTransport(Protocol):
    def write(self, data: bytes) -> None: ...
    def read_until(self, marker: bytes, timeout: float = 2.0) -> bytes: ...


@dataclass(frozen=True)
class Elm327Response:
    raw: bytes
    lines: tuple[str, ...]


def normalize_hex_line(line: str) -> bytes:
    compact = "".join(line.split())
    if not compact or len(compact) % 2:
        raise Elm327Error("invalid hexadecimal response line")
    try:
        return bytes.fromhex(compact)
    except ValueError as exc:
        raise Elm327Error("non-hexadecimal response line") from exc


class Elm327Adapter:
    """Conservative ELM327 command layer; protocol selection remains explicit."""

    INIT_COMMANDS = (b"ATZ\r", b"ATE0\r", b"ATL0\r", b"ATS0\r")

    def __init__(self, transport: LineTransport):
        self.transport = transport

    def command(self, command: bytes, timeout: float = 2.0) -> Elm327Response:
        if not command or b"\r" not in command:
            command = command.rstrip(b"\r") + b"\r"
        self.transport.write(command)
        raw = self.transport.read_until(b">", timeout)
        lines = tuple(
            line.strip().decode("ascii", errors="replace")
            for line in raw.replace(b"\r", b"\n").splitlines()
            if line.strip()
        )
        return Elm327Response(raw, lines)

    def initialize(self) -> list[Elm327Response]:
        return [self.command(command) for command in self.INIT_COMMANDS]

    def send_obd(self, payload: bytes) -> Elm327Response:
        if not payload:
            raise Elm327Error("empty OBD payload")
        return self.command(payload.hex().encode("ascii"))
