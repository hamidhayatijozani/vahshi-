import unittest

from iadp.diagnostics.session import DiagnosticSession
from iadp.sim import VirtualEcu


class TestVirtualEcuDtc(unittest.TestCase):
    def test_read_dtcs(self):
        codes = DiagnosticSession(VirtualEcu()).read_dtcs()
        self.assertEqual(codes[0].code, "012345")
        self.assertEqual(codes[0].status, 0x2F)


if __name__ == "__main__":
    unittest.main()
