import periphery

from periphery import GPIO
from periphery import PWM

# Open GPIO /dev/gpiochip0 line 10 with input direction
gpio_in = GPIO("/dev/gpiochip0", 10, "in")
# Open GPIO /dev/gpiochip0 line 12 with output direction
gpio_out = GPIO("/dev/gpiochip0", 12, "out")

value = gpio_in.read()
gpio_out.write(not value)

gpio_in.close()
gpio_out.close()