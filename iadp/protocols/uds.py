from __future__ import annotations

class UdsError(ValueError): pass

def positive_response(request_sid: int, response: bytes) -> bool:
    return bool(response) and response[0] == ((request_sid + 0x40) & 0xFF)

def negative_response(response: bytes) -> tuple[int, int] | None:
    if len(response) >= 3 and response[0] == 0x7F:
        return response[1], response[2]
    return None

def make_read_data_by_identifier(did: int) -> bytes:
    if not 0 <= did <= 0xFFFF:
        raise UdsError("DID out of range")
    return bytes((0x22, did >> 8, did & 0xFF))
