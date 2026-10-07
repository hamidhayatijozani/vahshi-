import unittest

from iadp.protocols.isotp import (
    IsoTpError,
    decode_consecutive_frame,
    decode_first_frame,
    decode_flow_control,
    encode_consecutive_frame,
    encode_first_frame,
    encode_flow_control,
    encode_single_frame,
    reassemble_classic_can,
)


class TestIsoTp(unittest.TestCase):
    def test_single_frame_round_trip(self):
        payload = bytes(range(7))
        self.assertEqual(encode_single_frame(payload), b"\x07\x00\x01\x02\x03\x04\x05\x06")
        
    def test_first_frame(self):
        ff = encode_first_frame(10, b"abcdef")
        decoded = decode_first_frame(ff)
        self.assertEqual(decoded.total_length, 10)
        self.assertEqual(decoded.payload, b"abcdef")

    def test_consecutive_frame(self):
        decoded = decode_consecutive_frame(encode_consecutive_frame(3, b"xyz"))
        self.assertEqual(decoded.sequence_number, 3)
        self.assertEqual(decoded.payload, b"xyz")

    def test_flow_control(self):
        decoded = decode_flow_control(encode_flow_control(0, 8, 0x0A))
        self.assertEqual((decoded.flow_status, decoded.block_size, decoded.st_min), (0, 8, 0x0A))

    def test_reassembly(self):
        payload = b"0123456789ABC"
        frames = [
            encode_first_frame(len(payload), payload[:6]),
            encode_consecutive_frame(1, payload[6:13]),
        ]
        self.assertEqual(reassemble_classic_can(frames), payload)

    def test_bad_sequence(self):
        with self.assertRaises(IsoTpError):
            reassemble_classic_can([
                encode_first_frame(10, b"abcdef"),
                encode_consecutive_frame(2, b"ghij"),
            ])


if __name__ == "__main__":
    unittest.main()
