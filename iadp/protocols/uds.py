from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class UdsError(ValueError):
    pass


class DiagnosticSessionType(IntEnum):
    DEFAULT = 0x01
    PROGRAMMING = 0x02
    EXTENDED = 0x03


NRC_NAMES = {
    0x10: "generalReject",
    0x11: "serviceNotSupported",
    0x12: "subFunctionNotSupported",
    0x13: "incorrectMessageLengthOrInvalidFormat",
    0x21: "busyRepeatRequest",
    0x22: "conditionsNotCorrect",
    0x24: "requestSequenceError",
    0x31: "requestOutOfRange",
    0x33: "securityAccessDenied",
    0x35: "invalidKey",
    0x36: "exceedNumberOfAttempts",
    0x37: "requiredTimeDelayNotExpired",
    0x78: "responsePending",
}


@dataclass(frozen=True)
class UdsNegativeResponse:
    service_id: int
    code: int

    @property
    def name(self) -> str:
        return NRC_NAMES.get(self.code, "unknown")


def positive_response(request_sid: int, response: bytes) -> bool:
    return bool(response) and response[0] == ((request_sid + 0x40) & 0xFF)


def negative_response(response: bytes) -> tuple[int, int] | None:
    if len(response) >= 3 and response[0] == 0x7F:
        return response[1], response[2]
    return None


def parse_negative_response(response: bytes) -> UdsNegativeResponse | None:
    parsed = negative_response(response)
    return UdsNegativeResponse(*parsed) if parsed else None


def require_positive_response(request_sid: int, response: bytes) -> bytes:
    negative = parse_negative_response(response)
    if negative:
        raise UdsError(f"UDS negative response 0x{negative.code:02X} ({negative.name})")
    if not positive_response(request_sid, response):
        raise UdsError(f"unexpected UDS response for SID 0x{request_sid:02X}")
    return response


def make_diagnostic_session_control(session: DiagnosticSessionType | int) -> bytes:
    value = int(session)
    if value not in {item.value for item in DiagnosticSessionType}:
        raise UdsError("unsupported diagnostic session")
    return bytes((0x10, value))


def make_tester_present(suppress_positive_response: bool = True) -> bytes:
    return bytes((0x3E, 0x80 if suppress_positive_response else 0x00))


def make_read_data_by_identifier(did: int) -> bytes:
    if not 0 <= did <= 0xFFFF:
        raise UdsError("DID out of range")
    return bytes((0x22, did >> 8, did & 0xFF))


def make_read_dtc_information(sub_function: int = 0x02) -> bytes:
    if not 0 <= sub_function <= 0xFF:
        raise UdsError("sub-function out of range")
    return bytes((0x19, sub_function))


def is_response_pending(response: bytes) -> bool:
    return len(response) >= 3 and response[:2] == bytes((0x7F, 0x00 | response[1])) and response[2] == 0x78
