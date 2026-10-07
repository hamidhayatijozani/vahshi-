from __future__ import annotations

from dataclasses import dataclass


PREFIX = "PCBU"


@dataclass(frozen=True)
class DiagnosticTroubleCode:
    code: str
    source: str
    raw: bytes
    status: int | None = None
    evidence_state: str = "observed"


def decode_obd_dtc(a: int, b: int) -> str:
    if not 0 <= a <= 0xFF or not 0 <= b <= 0xFF:
        raise ValueError("DTC bytes must be octets")
    system = PREFIX[(a >> 6) & 0x03]
    digit1 = (a >> 4) & 0x03
    digit2 = a & 0x0F
    return f"{system}{digit1}{digit2:X}{b:02X}"


def decode_obd_dtc_bytes(data: bytes) -> list[DiagnosticTroubleCode]:
    if len(data) % 2:
        raise ValueError("OBD DTC payload must contain pairs of bytes")
    result = []
    for index in range(0, len(data), 2):
        raw = data[index : index + 2]
        if raw == b"\x00\x00":
            continue
        result.append(DiagnosticTroubleCode(decode_obd_dtc(*raw), "OBD-II", raw))
    return result


def normalize_uds_dtc(raw_dtc: bytes, status: int | None = None) -> DiagnosticTroubleCode:
    if len(raw_dtc) != 3:
        raise ValueError("UDS DTC must contain three bytes")
    value = int.from_bytes(raw_dtc, "big")
    return DiagnosticTroubleCode(
        code=f"{value:06X}",
        source="UDS",
        raw=raw_dtc,
        status=status,
    )
