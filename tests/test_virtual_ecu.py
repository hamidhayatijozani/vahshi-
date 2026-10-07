import unittest

from iadp.diagnostics.identification import decode_uds_vin_response, make_obd_vin_request
from iadp.diagnostics.session import DiagnosticSession
from iadp.protocols.obd2 import decode_rpm, decode_speed
from iadp.sim import VirtualEcu


class TestVirtualEcu(unittest.TestCase):
    def test_obd_simulation(self):
        ecu = VirtualEcu()
        self.assertEqual(decode_rpm(ecu.request(b"\x01\x0C")), 1726.0)
        self.assertEqual(decode_speed(ecu.request(b"\x01\x0D")), 60)

    def test_uds_vin(self):
        ecu = VirtualEcu()
        session = DiagnosticSession(ecu)
        response = session.read_data_by_identifier(0xF190)
        self.assertEqual(decode_uds_vin_response(response), "SIMULATED-VIN")

    def test_obd_vin_request(self):
        self.assertEqual(make_obd_vin_request(), b"\x09\x02")


if __name__ == "__main__":
    unittest.main()
