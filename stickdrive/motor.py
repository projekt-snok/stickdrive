from smbus2 import SMBus
import struct
from stickdrive.utils import current_milli_time


class Driver:
    def __init__(self, address=0x04):
        self.bus = SMBus(1)
        self.address = address

        self.speed = 200
        self.direction = -55
        self.last_write = current_milli_time()
        self.next_read = self.last_write + 500

    def loop(self):
        now = current_milli_time()
        self._read_loop(now)

        if now > (self.last_write + 800):
            data = struct.pack('Bh', self.speed, self.direction)
            data = struct.unpack("B"*len(data), data)
            self.bus.write_i2c_block_data(self.address, 5, list(data))
            self.last_write = now
            self.next_read = now + 50
    
    def _read_loop(self, now):
        if now > self.next_read:
            response = self.bus.read_i2c_block_data(self.address, 4, 8)
            response = struct.unpack('BBBhh', ''.join(map(chr, response)))
            print "response:", response

            self.next_read = now + 10000


    def toggleEnable(self):
        self.bus.write_byte(self.address, 9)



