import time
import sys
import RPi.GPIO as GPIO

signals = {
 "egg": {"on":"000000000000000000000000", "long": 0.0008, "short": 0.0002, "pause":0.03, "off":"001001110011001101110100"},
}


SHORT_DELAY = 0.0001
CLK_DELAY = 0.00050
LONG_DELAY = 0.0003
EXTENDED_DELAY = 0.006

NUM_ATTEMPTS = 5
TRANSMIT_PIN = 23

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    sp_code, state = code.split("_")

    if "all" in code:
      [transmit_code(i + "_" + state) for i in signals.keys()]
      return ("all", state)

    else:

     #seq = code
     seq = signals.get(sp_code)
     long_delay = seq.get("long",LONG_DELAY)
     short_delay = seq.get("short", SHORT_DELAY)
     clk = seq.get("clk", CLK_DELAY)
     pause = seq.get("pause", EXTENDED_DELAY)
     data = seq.get(state)

     print "Transmitting: %s" % data

     for t in range(NUM_ATTEMPTS):
         print "Round: %s" % t
         for i in data:
             if i == '1':
                 GPIO.output(TRANSMIT_PIN, 1)
                 time.sleep(long_delay)
                 GPIO.output(TRANSMIT_PIN, 0)
                 time.sleep(short_delay)
             elif i == '0':
                 GPIO.output(TRANSMIT_PIN, 1)
                 time.sleep(short_delay)
                 GPIO.output(TRANSMIT_PIN, 0)
                 time.sleep(clk)
             else:
                 continue
         GPIO.output(TRANSMIT_PIN, 0)
         time.sleep(pause)
     GPIO.cleanup()

     return (sp_code, state)

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(\"' + str(argument) + '\")')
