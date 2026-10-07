import unittest

from iadp.diagnostics.session import DiagnosticSession
from iadp.protocols.uds import (
    DiagnosticSessionType,
    UdsError,
    is_response_pending,
    make_diagnostic_session_control,
    parse_negative_response,
)
from iadp.replay import ReplayExchange, ReplayExchangeEngine


class TestUdsSession(unittest.TestCase):
    def test_session_change(self):
        replay = ReplayExchangeEngine([
            ReplayExchange(b"\x10\x03", b"\x50\x03"),
        ])
        session = DiagnosticSession(replay)
        response = session.change_session(DiagnosticSessionType.EXTENDED)
        self.assertEqual(response, b"\x50\x03")
        self.assertEqual(session.session_type, DiagnosticSessionType.EXTENDED)

    def test_negative_response(self):
        parsed = parse_negative_response(b"\x7F\x22\x31")
        self.assertEqual((parsed.service_id, parsed.code, parsed.name), (0x22, 0x31, "requestOutOfRange"))

    def test_pending(self):
        self.assertTrue(is_response_pending(b"\x7F\x22\x78"))

    def test_replay_mismatch_is_fatal(self):
        replay = ReplayExchangeEngine([ReplayExchange(b"\x22\xF1\x90", b"\x62\xF1\x90VIN")])
        with self.assertRaises(ValueError):
            replay.request(b"\x22\xF1\x91")


if __name__ == "__main__":
    unittest.main()
