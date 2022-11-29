import periphery

from periphery import GPIO
from periphery import PWM


from motor import Motor
from wheel import Wheel

# Open GPIO /dev/gpiochip0 line 10 with input direction
gpio_in = GPIO("/dev/gpiochip0", 10, "in")
# Open GPIO /dev/gpiochip0 line 12 with output direction
gpio_out = GPIO("/dev/gpiochip0", 12, "out")

in1 = ["/dev/gpiochip2", 9]
in2 = ["/dev/gpiochip4", 10]
pwm = [1,0]

right_motor = Motor(in1, in2, pwm)
right_wheel = Wheel(right_motor)

value = gpio_in.read()
gpio_out.write(not value)

gpio_in.close()
gpio_out.close()