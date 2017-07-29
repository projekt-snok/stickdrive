import time, sys
from stickdrive.input import SixAxisResource, SixAxis
from stickdrive.motor import Driver
from stickdrive.utils import current_milli_time



class App:
    def __init__(self):
        self.last_time = current_milli_time()
        self.driver = Driver(address=0x04)

    def run(self):
        with SixAxisResource() as joystick:
            joystick.register_button_handler(self.toggle, SixAxis.BUTTON_CIRCLE)
            while 1:
                self.driver.loop()
                self.loop(joystick)

    def toggle(self, button):
        print 'Button! {}'.format(button)
        self.driver.toggleEnable()
    
    def loop(self, joystick):
        now = current_milli_time()
        if now > (self.last_time + 100):
            self.last_time = now
            # Default behaviour is to print the values of the four analogue axesi
            #print joystick
            
            #set direction on motor driver
            yValue = joystick.axes[1].corrected_value() #left stick Y-axis
            xValue = joystick.axes[2].corrected_value() #right stick X-axis
            
            self.driver.direction = int(round(254 * xValue))
            
            if yValue > 0:
                self.driver.speed = int(round(yValue * 254))
            else:
                self.driver.speed = 0
            
            print 'speed={}, direction={}'.format(self.driver.speed, self.driver.direction)



if __name__ == '__main__':
   app = App()
   app.run()

