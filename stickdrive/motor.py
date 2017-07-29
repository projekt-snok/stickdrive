import smbus
import struct
from stickdrive.utils import current_milli_time


class Driver:
    def __init__(self, address=0x04):
        self.bus = smbus.SMBus(1)
        self.address = address

        self.speed = 200
        self.direction = -55
        self.last = current_milli_time()

    def loop(self):
        now = current_milli_time()
        if now > (self.last + 700):
            data = struct.pack('Bh', self.speed, self.direction)
            data = struct.unpack("B"*len(data), data)
            self.bus.write_i2c_block_data(self.address, 5, list(data))
            response = self.bus.read_block_data(self.address, 4)
            print "response:", response 
            self.last = now


    def toggleEnable(self):
        self.bus.write_byte(self.address, 9)



