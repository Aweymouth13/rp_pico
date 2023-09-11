from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time
import os

# initialize the temperature sensor
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

def get_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)  # 400 kHz
oled = SSD1306_I2C(128, 64, i2c)

# find a suitable filename
file_index = 0
while True:
    try:
        os.stat('temp_{}.csv'.format(file_index))
        file_index += 1
    except OSError:
        break

filename = 'temp_{}.csv'.format(file_index)

start_time = time.time()
blink_flag = False

while True:
    # clear the display
    oled.fill(0)

    # get the current temperature in celsius
    temp_c = get_temperature()

    # convert the temperature to fahrenheit
    temp_f = (temp_c * 9/5) + 32

    # display the temperatures
    oled.text('The current temp is:', 0, 0)
    oled.text('{:.2f} C / {:.2f} F'.format(temp_c, temp_f), 0, 20)

    # blink the 'temp logged' message
    if blink_flag:
        oled.text('temp logged', 0, 40)
    blink_flag = not blink_flag

    # update the display to show the changes
    oled.show()

    # save the elapsed time and temperature in celsius to the file
    with open(filename, 'a') as f:
        elapsed_time = time.time() - start_time
        f.write('{:.2f}, {:.2f}\n'.format(elapsed_time, temp_c))

    # wait for a second before updating again
    time.sleep(0.5)
