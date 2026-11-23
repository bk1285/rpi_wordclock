"""Minimal DDP v1 RGB frame buffer (no discovery or timecodes)."""

import struct


class DDPFrame:
    """Apply byte-addressed DDP writes while retaining unchanged pixels."""

    HEADER = struct.Struct('!BBBBIH')

    def __init__(self, pixel_count):
        self.data = bytearray(pixel_count * 3)

    def apply(self, packet):
        """Return (push, has_data), or None for unsupported/invalid packets."""
        if len(packet) < self.HEADER.size:
            return None
        flags, sequence, data_type, destination, offset, length = self.HEADER.unpack_from(packet)
        if (flags & 0xc0) != 0x40 or flags & 0x3e:
            return None
        # Type 0 is commonly used for untyped RGB; 0x0b means RGB, 8 bits/channel.
        if sequence & 0xf0 or data_type not in (0, 0x0b) or destination not in (1, 255):
            return None
        if len(packet) != self.HEADER.size + length or offset + length > len(self.data):
            return None
        self.data[offset:offset + length] = packet[self.HEADER.size:]
        return bool(flags & 1), bool(length)
