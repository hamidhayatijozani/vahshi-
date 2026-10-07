from __future__ import annotations

class VirtualEcu:
    def __init__(self):
        self.data_identifiers = {0xF190: b"SIMULATED-VIN"}

    def request(self, payload: bytes) -> bytes:
        if payload[:1] == b"\x22" and len(payload) == 3:
            did = int.from_bytes(payload[1:], "big")
            value = self.data_identifiers.get(did)
            if value is None:
                return bytes((0x7F, 0x22, 0x31))
            return bytes((0x62, payload[1], payload[2])) + value
        return bytes((0x7F, payload[0] if payload else 0, 0x11))
