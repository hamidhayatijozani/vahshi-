from __future__ import annotations

def decode_rpm(response: bytes) -> float:
    if len(response) < 4 or response[0:2] != bytes((0x41, 0x0C)):
        raise ValueError("invalid RPM response")
    return ((response[2] << 8) | response[3]) / 4.0

def decode_speed(response: bytes) -> int:
    if len(response) < 3 or response[0:2] != bytes((0x41, 0x0D)):
        raise ValueError("invalid speed response")
    return response[2]
