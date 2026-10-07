from __future__ import annotations

from dataclasses import dataclass


class IsoTpError(ValueError):
    """Invalid or incomplete ISO-TP frame/state."""


@dataclass(frozen=True)
class SingleFrame:
    payload: bytes


@dataclass(frozen=True)
class FirstFrame:
    total_length: int
    payload: bytes


@dataclass(frozen=True)
class ConsecutiveFrame:
    sequence_number: int
    payload: bytes


@dataclass(frozen=True)
class FlowControlFrame:
    flow_status: int
    block_size: int
    st_min: int


def decode_single_frame(frame: bytes) -> SingleFrame:
    if not frame:
        raise IsoTpError("empty ISO-TP frame")
    pci_type = frame[0] >> 4
    if pci_type != 0:
        raise IsoTpError("not a single frame")
    length = frame[0] & 0x0F
    if length > len(frame) - 1:
        raise IsoTpError("declared payload exceeds frame")
    return SingleFrame(frame[1 : 1 + length])


def decode_first_frame(frame: bytes) -> FirstFrame:
    if len(frame) < 2 or frame[0] >> 4 != 1:
        raise IsoTpError("not a first frame")
    total_length = ((frame[0] & 0x0F) << 8) | frame[1]
    if total_length <= 7:
        raise IsoTpError("first frame length must exceed single-frame capacity")
    payload = frame[2:]
    if len(payload) > min(6, total_length):
        payload = payload[:6]
    return FirstFrame(total_length, payload)


def decode_consecutive_frame(frame: bytes) -> ConsecutiveFrame:
    if len(frame) < 2 or frame[0] >> 4 != 2:
        raise IsoTpError("not a consecutive frame")
    return ConsecutiveFrame(frame[0] & 0x0F, frame[1:])


def decode_flow_control(frame: bytes) -> FlowControlFrame:
    if len(frame) < 3 or frame[0] >> 4 != 3:
        raise IsoTpError("not a flow-control frame")
    flow_status = frame[0] & 0x0F
    if flow_status > 2:
        raise IsoTpError("reserved flow status")
    return FlowControlFrame(flow_status, frame[1], frame[2])


def encode_single_frame(payload: bytes) -> bytes:
    if len(payload) > 7:
        raise IsoTpError("classic CAN single frame payload exceeds 7 bytes")
    return bytes([len(payload)]) + payload


def encode_first_frame(total_length: int, payload: bytes) -> bytes:
    if not 8 <= total_length <= 0xFFF:
        raise IsoTpError("total length out of classic ISO-TP range")
    if len(payload) > 6:
        raise IsoTpError("first frame payload exceeds 6 bytes")
    if len(payload) > total_length:
        raise IsoTpError("payload exceeds declared total length")
    return bytes([0x10 | (total_length >> 8), total_length & 0xFF]) + payload


def encode_consecutive_frame(sequence_number: int, payload: bytes) -> bytes:
    if not 0 <= sequence_number <= 0x0F:
        raise IsoTpError("sequence number out of range")
    if len(payload) > 7:
        raise IsoTpError("consecutive-frame payload exceeds 7 bytes")
    return bytes([0x20 | sequence_number]) + payload


def encode_flow_control(flow_status: int, block_size: int, st_min: int) -> bytes:
    if flow_status not in (0, 1, 2):
        raise IsoTpError("reserved flow status")
    if not 0 <= block_size <= 0xFF or not 0 <= st_min <= 0xFF:
        raise IsoTpError("flow-control field out of range")
    return bytes([0x30 | flow_status, block_size, st_min])


def reassemble_classic_can(frames: list[bytes]) -> bytes:
    """Reassemble a complete classic-CAN ISO-TP payload from received frames."""
    if not frames:
        raise IsoTpError("no frames")
    first = frames[0]
    if first[0] >> 4 == 0:
        return decode_single_frame(first).payload
    ff = decode_first_frame(first)
    payload = bytearray(ff.payload)
    expected_sn = 1
    for frame in frames[1:]:
        cf = decode_consecutive_frame(frame)
        if cf.sequence_number != expected_sn:
            raise IsoTpError(
                f"unexpected sequence number {cf.sequence_number}, expected {expected_sn}"
            )
        payload.extend(cf.payload)
        expected_sn = (expected_sn + 1) & 0x0F
        if len(payload) >= ff.total_length:
            return bytes(payload[: ff.total_length])
    raise IsoTpError(
        f"incomplete payload: received {len(payload)} of {ff.total_length} bytes"
    )
