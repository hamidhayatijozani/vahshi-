from __future__ import annotations

_PREFIX = "PCBU"

def decode_obd_dtc(a: int, b: int) -> str:
    if not 0 <= a <= 255 or not 0 <= b <= 255:
        raise ValueError("DTC bytes must be octets")
    system = _PREFIX[(a >> 6) & 3]
    d1 = (a >> 4) & 3
    d2 = a & 0x0F
    return f"{system}{d1}{d2:X}{b:02X}"
