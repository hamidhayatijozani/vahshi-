import unittest

from iadp.adapters.elm327 import Elm327Adapter, normalize_hex_line


class FakeTransport:
    def __init__(self):
        self.writes = []
        self.response = b"41 0C 1A F8\r>"

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    def read_until(self, marker: bytes, timeout: float = 2.0) -> bytes:
        return self.response


class TestElm327(unittest.TestCase):
    def test_normalize_hex(self):
        self.assertEqual(normalize_hex_line("41 0C 1A F8"), b"\x41\x0c\x1a\xf8")

    def test_command(self):
        transport = FakeTransport()
        response = Elm327Adapter(transport).send_obd(b"\x01\x0c")
        self.assertEqual(transport.writes[-1], b"010c\r")
        self.assertEqual(response.lines, ("41 0C 1A F8", ">"))


if __name__ == "__main__":
    unittest.main()
