import unittest

from iadp.diagnostics.dtc import decode_obd_dtc, decode_obd_dtc_bytes, decode_uds_report_dtc


class TestDtc(unittest.TestCase):
    def test_obd_dtc(self):
        self.assertEqual(decode_obd_dtc(0x01, 0x23), "P0123")

    def test_obd_dtc_list(self):
        codes = decode_obd_dtc_bytes(bytes.fromhex("0123 0000"))
        self.assertEqual([item.code for item in codes], ["P0123"])

    def test_uds_dtc_report(self):
        result = decode_uds_report_dtc(bytes.fromhex("59 02 FF 01 23 45 2F"))
        self.assertEqual(result[0].code, "012345")
        self.assertEqual(result[0].status, 0x2F)


if __name__ == "__main__":
    unittest.main()
