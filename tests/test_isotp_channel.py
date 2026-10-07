import unittest

from iadp.transport.base import CanFrame, MemoryCanTransport
from iadp.transport.isotp_channel import IsoTpChannel


class TestIsoTpChannel(unittest.TestCase):
    def test_single_frame_request_response(self):
        bus = MemoryCanTransport()
        bus.queue(CanFrame(0x7E8, b"\x03\x62\xF1\x90"))
        response = IsoTpChannel(bus, 0x7E0, 0x7E8).request(b"\x22\xF1\x90")
        self.assertEqual(response, b"\x62\xF1\x90")
        self.assertEqual(bus.sent[0].data, b"\x03\x22\xF1\x90")

    def test_multi_frame_response_sends_flow_control(self):
        bus = MemoryCanTransport()
        bus.queue(
            CanFrame(0x7E8, b"\x10\x0Aabcdefgh"),
            CanFrame(0x7E8, b"\x21ij"),
        )
        response = IsoTpChannel(bus, 0x7E0, 0x7E8).request(b"\x22\xF1\x90")
        self.assertEqual(response, b"abcdefghij")
        self.assertEqual(bus.sent[-1].data, b"\x30\x00\x00")


if __name__ == "__main__":
    unittest.main()
