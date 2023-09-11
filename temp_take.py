import machine
import utime
import os

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
start_time = utime.time()

led = machine.Pin(25, machine.Pin.OUT)

def get_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

def get_filename():
    i = 0
    while True:
        filename = f'temp_{i}.csv'
        try:
            os.stat(filename)
            i += 1
        except OSError:
            break
    return filename


filename = get_filename()
with open(filename, 'w') as f:
    f.write('delta t (min),temp (c)\n')

while True:
    delta_t = (utime.time() - start_time) / 60
    temperature = get_temperature()
    with open(filename, 'a') as f:
        f.write(f'{delta_t:.2f},{temperature:.2f}\n')
    
    led.value(1)
    utime.sleep(0.5)
    led.value(0)
    
    utime.sleep(4.5)
