from __future__ import annotations
from dataclasses import dataclass

class IsoTpError(ValueError): pass

@dataclass(frozen=True)
class SingleFrame:
    payload: bytes

def decode_single_frame(frame: bytes) -> SingleFrame:
    if not frame:
        raise IsoTpError("empty ISO-TP frame")
    pci_type = frame[0] >> 4
    if pci_type != 0:
        raise IsoTpError("not a single frame")
    length = frame[0] & 0x0F
    if length > len(frame) - 1:
        raise IsoTpError("declared payload exceeds frame")
    return SingleFrame(frame[1:1+length])
