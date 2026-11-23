# DDP receiver

Select `ddp` in the plugin menu or by sending `{"name":"ddp"}` to
`POST /api/plugin`. The receiver listens on UDP port 4048 while selected.
After the first valid data packet, it returns to the clock after 10 seconds
without pixel data. Before the first packet it waits until manually exited.

Configure `[plugin_ddp]` in `wordclock_config/wordclock_config.cfg` to override
`port` or `timeout_seconds`. The existing display brightness applies. Pixel
data is 8-bit RGB: the matrix is row-major from the upper left, followed by
the four minute LEDs. For an 11x10 clock, send up to 114 RGB pixels (342 bytes).
DDP v1 writes to destination 1 or 255 are supported with type 0 or RGB 8-bit
(0x0b), including byte offsets and push-only packets. The buffer persists
between pushes. Queries, storage, timecodes and other color formats are ignored.
