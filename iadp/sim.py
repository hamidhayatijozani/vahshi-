from __future__ import annotations


class VirtualEcu:
    def __init__(self):
        self.data_identifiers = {0xF190: b"SIMULATED-VIN"}
        self.session = 0x01
        self.rpm = 1726
        self.speed = 60

    def request(self, payload: bytes) -> bytes:
        if not payload:
            return b""
        sid = payload[0]

        if sid == 0x10 and len(payload) == 2:
            if payload[1] not in (0x01, 0x02, 0x03):
                return b"\x7F\x10\x12"
            self.session = payload[1]
            return bytes((0x50, self.session))

        if sid == 0x3E and len(payload) == 2:
            if payload[1] & 0x80:
                return b""
            return b"\x7E\x00"

        if sid == 0x22 and len(payload) == 3:
            did = int.from_bytes(payload[1:], "big")
            value = self.data_identifiers.get(did)
            if value is None:
                return b"\x7F\x22\x31"
            return bytes((0x62, payload[1], payload[2])) + value

        if sid == 0x19 and len(payload) == 2:
            if payload[1] == 0x02:
                return bytes.fromhex("59 02 FF 01 23 45 2F")
            return bytes((0x7F, 0x19, 0x12))

        if sid == 0x01 and len(payload) == 2:
            pid = payload[1]
            if pid == 0x0C:
                raw = int(self.rpm * 4).to_bytes(2, "big")
                return b"\x41\x0C" + raw
            if pid == 0x0D:
                return bytes((0x41, 0x0D, self.speed))
            return bytes((0x7F, 0x01, 0x31))

        return bytes((0x7F, sid, 0x11))
