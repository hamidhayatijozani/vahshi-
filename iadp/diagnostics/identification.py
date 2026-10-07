from __future__ import annotations

from dataclasses import dataclass

from iadp.protocols.obd2 import make_vehicle_information_request
from iadp.protocols.uds import make_read_data_by_identifier


@dataclass(frozen=True)
class IdentificationResult:
    method: str
    value: str | None
    raw_response: bytes
    evidence_state: str = "observed"


def decode_obd_vin_response(response: bytes) -> str:
    """Decode the common OBD-II Mode 09 PID 02 VIN response payload."""
    if len(response) < 3 or response[0:2] != bytes((0x49, 0x02)):
        raise ValueError("invalid OBD VIN response")
    raw = response[2:]
    text = bytes(b for b in raw if 0x20 <= b <= 0x7E).decode("ascii", errors="strict").strip()
    if not text:
        raise ValueError("VIN response contains no printable identifier")
    return text


def make_obd_vin_request() -> bytes:
    return make_vehicle_information_request(0x02)


def make_uds_vin_request(did: int = 0xF190) -> bytes:
    return make_read_data_by_identifier(did)


def decode_uds_vin_response(response: bytes, did: int = 0xF190) -> str:
    prefix = bytes((0x62, did >> 8, did & 0xFF))
    if not response.startswith(prefix):
        raise ValueError("unexpected UDS VIN response")
    value = response[3:].decode("ascii", errors="strict").strip()
    if not value:
        raise ValueError("empty UDS VIN")
    return value
