from smbus2 import SMBus
import struct
from stickdrive.utils import current_milli_time

SPEED_FORMAT = 'h'
DIRECTION_FORMAT = 'h'
CMD_FORMAT = 'B'
STATUS_FORMAT = 'B'

CMD_STATUS_REQUEST = 4
CMD_VECTOR = 5
CMD_ENABLE = 9

class Driver:
    def __init__(self, address=0x04):
        self.bus = SMBus(1)
        self.address = address

        self.speed = 200
        self.direction = -55
        self.last_write = current_milli_time()
        self.next_read = self.last_write + 500

        self.read_template = CMD_FORMAT + STATUS_FORMAT + SPEED_FORMAT + DIRECTION_FORMAT
        self.read_size = struct.calcsize(self.read_template)
        self.vector_template = SPEED_FORMAT + DIRECTION_FORMAT
        

    def loop(self):
        now = current_milli_time()
        self._read_loop(now)

        #send vector
        if now > (self.last_write + 300):
            data = struct.pack(self.vector_template, self.speed, self.direction)
            data = struct.unpack("B"*len(data), data) #make int to bytes
            self.bus.write_i2c_block_data(self.address, CMD_VECTOR, list(data)) 
            self.last_write = now
            self.next_read = now + 50


    def _read_loop(self, now):
        if now > self.next_read:
            response = self.bus.read_i2c_block_data(self.address, CMD_STATUS_REQUEST, self.read_size)
            response = struct.unpack(self.read_template, ''.join(map(chr, response)))
            print "response:", response

            self.next_read = now + 10000


    def toggleEnable(self):
        self.bus.write_byte(self.address, CMD_ENABLE)



