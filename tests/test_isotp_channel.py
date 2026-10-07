import unittest

from iadp.transport.base import CanFrame, MemoryCanTransport
from iadp.transport.isotp_channel import IsoTpChannel


class TestIsoTpChannel(unittest.TestCase):
    def test_single_frame_request_response(self):
        bus = MemoryCanTransport()
        bus.queue(CanFrame(0x7E8, b"\x03\x62\xF1\x90"))
        channel = IsoTpChannel(bus, 0x7E0, 0x7E8)
        response = channel.request(b"\x22\xF1\x90")
        self.assertEqual(response, b"\x62\xF1\x90")
        self.assertEqual(bus.sent[0].arbitration_id, 0x7E0)
        self.assertEqual(bus.sent[0].data, b"\x03\x22\xF1\x90")


if __name__ == "__main__":
    unittest.main()
