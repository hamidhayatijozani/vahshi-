from __future__ import annotations

import time

from iadp.protocols.isotp import (
    IsoTpError,
    decode_consecutive_frame,
    decode_first_frame,
    decode_flow_control,
    decode_single_frame,
    encode_consecutive_frame,
    encode_first_frame,
    encode_flow_control,
    encode_single_frame,
    reassemble_classic_can,
)
from iadp.transport.base import CanFrame, CanTransport


def _st_min_seconds(value: int) -> float:
    if value <= 0x7F:
        return value / 1000.0
    if 0xF1 <= value <= 0xF9:
        return (value - 0xF0) / 10000.0
    raise IsoTpError("unsupported STmin encoding")


class IsoTpChannel:
    """Classic-CAN ISO-TP request/response channel over an abstract CAN transport."""

    def __init__(
        self,
        transport: CanTransport,
        tx_id: int,
        rx_id: int,
        *,
        extended_id: bool = False,
        timeout: float = 1.0,
    ) -> None:
        self.transport = transport
        self.tx_id = tx_id
        self.rx_id = rx_id
        self.extended_id = extended_id
        self.timeout = timeout

    def _send(self, data: bytes) -> None:
        self.transport.send_frame(
            CanFrame(self.tx_id, data, is_extended_id=self.extended_id)
        )

    def _receive(self, deadline: float) -> bytes:
        while time.monotonic() < deadline:
            frame = self.transport.receive_frame(max(0.0, deadline - time.monotonic()))
            if frame is None:
                continue
            if frame.arbitration_id == self.rx_id:
                return frame.data
        raise TimeoutError("ISO-TP receive timeout")

    def _send_payload(self, payload: bytes) -> None:
        if len(payload) <= 7:
            self._send(encode_single_frame(payload))
            return

        self._send(encode_first_frame(len(payload), payload[:6]))
        offset = 6
        sequence = 1
        deadline = time.monotonic() + self.timeout
        while offset < len(payload):
            fc = decode_flow_control(self._receive(deadline))
            if fc.flow_status == 1:
                deadline = time.monotonic() + self.timeout
                continue
            if fc.flow_status == 2:
                raise IsoTpError("receiver overflow/abort")
            delay = _st_min_seconds(fc.st_min)
            sent_in_block = 0
            while offset < len(payload) and (fc.block_size == 0 or sent_in_block < fc.block_size):
                chunk = payload[offset : offset + 7]
                self._send(encode_consecutive_frame(sequence, chunk))
                offset += len(chunk)
                sequence = (sequence + 1) & 0x0F
                sent_in_block += 1
                if offset < len(payload) and delay:
                    time.sleep(delay)
                if time.monotonic() >= deadline:
                    raise TimeoutError("ISO-TP flow-control timeout")
            deadline = time.monotonic() + self.timeout

    def request(self, payload: bytes) -> bytes:
        if not payload:
            raise IsoTpError("empty ISO-TP payload")
        self._send_payload(payload)
        first = self._receive(time.monotonic() + self.timeout)
        if first[0] >> 4 == 0:
            return decode_single_frame(first).payload
        if first[0] >> 4 != 1:
            raise IsoTpError("unexpected response PCI")
        ff = decode_first_frame(first)
        self._send(encode_flow_control(0, 0, 0))
        frames = [first]
        received = len(ff.payload)
        deadline = time.monotonic() + self.timeout
        expected = 1
        while received < ff.total_length:
            frame = self._receive(deadline)
            cf = decode_consecutive_frame(frame)
            if cf.sequence_number != expected:
                raise IsoTpError(
                    f"unexpected sequence number {cf.sequence_number}, expected {expected}"
                )
            frames.append(frame)
            received += len(cf.payload)
            expected = (expected + 1) & 0x0F
            deadline = time.monotonic() + self.timeout
        return reassemble_classic_can(frames)
