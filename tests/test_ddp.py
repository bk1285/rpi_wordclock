import socket
import struct
import threading
import time
import unittest

from wordclock_plugins.ddp.plugin import plugin
from wordclock_plugins.ddp.receiver import DDPFrame


def packet(data=b'', offset=0, flags=0x41, data_type=0x0b, destination=1,
           sequence=0, length=None):
    return struct.pack('!BBBBIH', flags, sequence, data_type, destination,
                       offset, len(data) if length is None else length) + data


class FrameTests(unittest.TestCase):
    def test_full_frame_and_untyped_rgb(self):
        frame = DDPFrame(114)
        data = bytes(i % 256 for i in range(342))
        self.assertEqual(frame.apply(packet(data, data_type=0)), (True, True))
        self.assertEqual(frame.data, data)

    def test_split_unaligned_partial_updates_and_empty_push(self):
        frame = DDPFrame(3)
        self.assertEqual(frame.apply(packet(b'\x01\x02\x03\x04', flags=0x40)), (False, True))
        self.assertEqual(frame.apply(packet(b'\x05\x06', offset=4, flags=0x40)), (False, True))
        self.assertEqual(frame.apply(packet(b'', destination=255)), (True, False))
        self.assertEqual(frame.data, b'\x01\x02\x03\x04\x05\x06\x00\x00\x00')
        self.assertEqual(frame.apply(packet(b'\xff', offset=2)), (True, True))
        self.assertEqual(frame.data, b'\x01\x02\xff\x04\x05\x06\x00\x00\x00')

    def test_rejects_invalid_without_altering_buffer(self):
        frame = DDPFrame(2)
        frame.apply(packet(b'\x01\x02\x03'))
        before = bytes(frame.data)
        invalid = [
            b'', packet(b'\x01', flags=0x01), packet(b'\x01', flags=0x81),
            packet(b'\x01', flags=0x51), packet(b'\x01', flags=0x49),
            packet(b'\x01', flags=0x45), packet(b'\x01', flags=0x43),
            packet(b'\x01', data_type=0x1b), packet(b'\x01', destination=250),
            packet(b'\x01', sequence=16), packet(b'\x01', offset=6),
            packet(b'\x01', length=2), packet(b'\x01') + b'\x02',
        ]
        for raw in invalid:
            with self.subTest(raw=raw):
                self.assertIsNone(frame.apply(raw))
                self.assertEqual(frame.data, before)


class Display:
    def __init__(self):
        self.frame = None
        self.shown = threading.Event()

    def get_wca_width(self): return 11
    def get_wca_height(self): return 10

    def show_rgb_frame(self, frame):
        self.frame = bytes(frame)
        self.shown.set()


class Events:
    EVENT_BUTTON_RETURN = 2
    EVENT_EXIT_PLUGIN = 3
    EVENT_NEXT_PLUGIN_REQUESTED = 4

    def __init__(self): self.event = -1
    def waitForEvent(self, _): return self.event


class Config:
    def __init__(self, port, timeout=1): self.values = {'port': port, 'timeout_seconds': timeout}
    def getint(self, section, key): return self.values[key]


class PluginTests(unittest.TestCase):
    def test_socket_receives_split_frame_then_times_out(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reserve:
            reserve.bind(('127.0.0.1', 0))
            port = reserve.getsockname()[1]
        display, events = Display(), Events()
        receiver = plugin(Config(port))
        thread = threading.Thread(target=receiver.run, args=(display, events), daemon=True)
        thread.start()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            deadline = time.monotonic() + 2
            while not display.shown.is_set() and time.monotonic() < deadline:
                sender.sendto(packet(b'\x01\x02\x03', flags=0x40), ('127.0.0.1', port))
                sender.sendto(packet(b'\x04\x05\x06', offset=330), ('127.0.0.1', port))
                display.shown.wait(0.05)
        self.assertTrue(display.shown.is_set())
        self.assertEqual(display.frame, b'\x01\x02\x03' + bytes(327) + b'\x04\x05\x06' + bytes(9))
        thread.join(3)
        self.assertFalse(thread.is_alive(), 'receiver did not return after inactivity')

    def test_manual_exit_without_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reserve:
            reserve.bind(('127.0.0.1', 0))
            port = reserve.getsockname()[1]
        events = Events()
        thread = threading.Thread(target=plugin(Config(port)).run, args=(Display(), events), daemon=True)
        thread.start()
        # No initial packet: even the configured timeout must not exit DDP.
        time.sleep(1.2)
        self.assertTrue(thread.is_alive())
        events.event = events.EVENT_NEXT_PLUGIN_REQUESTED
        thread.join(2)
        self.assertFalse(thread.is_alive(), 'manual plugin switch did not exit')

    def test_busy_port_returns_to_default_plugin(self):
        class TransitionEvents(Events):
            next_action = 'next_plugin'

            def waitForEvent(self, _):
                self.next_action = 'default'
                return self.event

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reserve:
            reserve.bind(('', 0))
            events = TransitionEvents()
            with self.assertLogs(level='ERROR'):
                plugin(Config(reserve.getsockname()[1])).run(Display(), events)
            self.assertEqual(events.next_action, 'default')


if __name__ == '__main__':
    unittest.main()
