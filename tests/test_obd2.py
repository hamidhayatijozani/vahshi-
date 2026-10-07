import unittest
from iadp.protocols.obd2 import decode_rpm, decode_speed

class TestOBD2(unittest.TestCase):
    def test_rpm(self):
        self.assertEqual(decode_rpm(bytes([0x41,0x0C,0x1A,0xF8])), 1726.0)

    def test_speed(self):
        self.assertEqual(decode_speed(bytes([0x41,0x0D,0x3C])), 60)

if __name__ == "__main__":
    unittest.main()
