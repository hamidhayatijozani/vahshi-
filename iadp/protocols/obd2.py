from __future__ import annotations


class Obd2Error(ValueError):
    pass


def make_current_data_request(pid: int) -> bytes:
    if not 0 <= pid <= 0xFF:
        raise Obd2Error("PID out of range")
    return bytes((0x01, pid))


def make_freeze_frame_request(pid: int) -> bytes:
    if not 0 <= pid <= 0xFF:
        raise Obd2Error("PID out of range")
    return bytes((0x02, pid))


def make_vehicle_information_request(info_type: int) -> bytes:
    if not 0 <= info_type <= 0xFF:
        raise Obd2Error("information type out of range")
    return bytes((0x09, info_type))


def make_clear_dtc_request() -> bytes:
    return bytes((0x04,))


def decode_rpm(response: bytes) -> float:
    if len(response) < 4 or response[0:2] != bytes((0x41, 0x0C)):
        raise Obd2Error("invalid RPM response")
    return ((response[2] << 8) | response[3]) / 4.0


def decode_speed(response: bytes) -> int:
    if len(response) < 3 or response[0:2] != bytes((0x41, 0x0D)):
        raise Obd2Error("invalid speed response")
    return response[2]


def decode_coolant_temperature(response: bytes) -> int:
    if len(response) < 3 or response[0:2] != bytes((0x41, 0x05)):
        raise Obd2Error("invalid coolant-temperature response")
    return response[2] - 40


def decode_throttle_position(response: bytes) -> float:
    if len(response) < 3 or response[0:2] != bytes((0x41, 0x11)):
        raise Obd2Error("invalid throttle-position response")
    return response[2] * 100.0 / 255.0
