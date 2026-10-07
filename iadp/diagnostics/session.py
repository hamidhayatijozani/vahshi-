from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from iadp.protocols.uds import (
    DiagnosticSessionType,
    make_diagnostic_session_control,
    make_read_data_by_identifier,
    make_tester_present,
    parse_negative_response,
    require_positive_response,
)


class Exchange(Protocol):
    def request(self, payload: bytes) -> bytes: ...


@dataclass
class DiagnosticSession:
    exchange: Exchange
    session_type: DiagnosticSessionType = DiagnosticSessionType.DEFAULT

    def change_session(self, session_type: DiagnosticSessionType) -> bytes:
        response = self.exchange.request(make_diagnostic_session_control(session_type))
        payload = require_positive_response(0x10, response)
        self.session_type = session_type
        return payload

    def tester_present(self, suppress_positive_response: bool = True) -> bytes:
        response = self.exchange.request(make_tester_present(suppress_positive_response))
        if suppress_positive_response and response == b"":
            return response
        return require_positive_response(0x3E, response)

    def read_data_by_identifier(self, did: int) -> bytes:
        response = self.exchange.request(make_read_data_by_identifier(did))
        return require_positive_response(0x22, response)

    @staticmethod
    def negative_response(response: bytes):
        return parse_negative_response(response)
