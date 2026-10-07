import unittest
from iadp.protocols.isotp import decode_single_frame
from iadp.protocols.uds import make_read_data_by_identifier, positive_response, negative_response
from iadp.diagnostics.session import DiagnosticSession
from iadp.sim import VirtualEcu

class TestProtocols(unittest.TestCase):
    def test_isotp_single_frame(self):
        frame = bytes([3, 1, 2, 3, 0, 0, 0, 0])
        self.assertEqual(decode_single_frame(frame).payload, bytes([1,2,3]))

    def test_uds_request(self):
        self.assertEqual(make_read_data_by_identifier(0xF190), bytes([0x22,0xF1,0x90]))

    def test_virtual_ecu_vin(self):
        response = DiagnosticSession(VirtualEcu()).read_data_by_identifier(0xF190)
        self.assertTrue(positive_response(0x22, response))
        self.assertEqual(response[3:], b"SIMULATED-VIN")

    def test_uds_negative(self):
        self.assertEqual(negative_response(bytes([0x7F,0x22,0x31])), (0x22,0x31))

if __name__ == "__main__":
    unittest.main()
