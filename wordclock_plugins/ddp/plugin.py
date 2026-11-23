"""Show DDP RGB frames while this plugin is selected."""

import logging
import socket
import time

from wordclock_plugins.ddp.receiver import DDPFrame


class plugin:
    def __init__(self, config):
        self.name = 'ddp'
        self.pretty_name = 'DDP'
        self.description = 'Display RGB frames received via DDP.'
        self.port = config.getint('plugin_ddp', 'port')
        self.timeout = config.getint('plugin_ddp', 'timeout_seconds')
        if not 1 <= self.port <= 65535 or self.timeout < 1:
            raise ValueError('DDP port must be 1-65535 and timeout_seconds at least 1')

    def run(self, display, events):
        frame = DDPFrame(display.get_wca_width() * display.get_wca_height() + 4)
        # Read one extra byte so an oversized datagram cannot look valid after truncation.
        packet_size = DDPFrame.HEADER.size + len(frame.data) + 1
        last_data = None
        rendered = 0
        exit_events = (events.EVENT_BUTTON_RETURN, events.EVENT_EXIT_PLUGIN,
                       events.EVENT_NEXT_PLUGIN_REQUESTED)
        # Clear the previous plugin transition even if binding fails. Otherwise
        # the main loop can keep retrying this plugin instead of the clock.
        if events.waitForEvent(0) in exit_events:
            return
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(('', self.port))
                sock.settimeout(0.1)
                logging.info('DDP listening on UDP port %d', self.port)
                while True:
                    event = events.waitForEvent(0)
                    if event in exit_events:
                        return
                    if last_data is not None and time.monotonic() - last_data >= self.timeout:
                        logging.info('DDP timed out; returning to the clock')
                        return
                    try:
                        packet = sock.recv(packet_size)
                    except socket.timeout:
                        continue
                    result = frame.apply(packet)
                    if result is None:
                        continue
                    push, has_data = result
                    if has_data:
                        last_data = time.monotonic()
                    if push:
                        display.show_rgb_frame(frame.data)
                        rendered += 1
        except OSError:
            logging.exception('DDP socket failed; returning to the clock')
        finally:
            if rendered:
                logging.info('DDP displayed %d frames', rendered)
