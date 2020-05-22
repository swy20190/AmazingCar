import RPi.GPIO as GPIO
import basic
from math import pi

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

# first, we must test the speed of the car
if __name__ == '__main__':
    basic.init()
    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)
    # forward 1 meter
    # R = 65mm
    time_ward = 990.0/(90 / 48 * pi * 65)  # 由于惯性提前刹车，48是齿轮减速比
    basic.forward(speed=90, duration=time_ward, l_m=L_Motor, r_m=R_Motor)
    # 1st brake
    basic.brake(2.0, L_Motor, R_Motor)
    # backward 1 meter
    basic.backward(90, time_ward, L_Motor, R_Motor)
    # 2nd brake
    basic.brake(2.0, L_Motor, R_Motor)
    # turn left by 135 degree
    # speed of car
    turning_time = 0.75 * 1000 / (87.006 / 48 * 65)
    basic.advanced_turn(direction=0, duration=turning_time, l_m=L_Motor, r_m=R_Motor)
    # 3rd brake
    basic.brake(2.0, L_Motor, R_Motor)
    # turn right by 135 degree
    basic.advanced_turn(direction=1, duration=turning_time, l_m=L_Motor, r_m=R_Motor)
    # 4nd brake
    basic.brake(2.0, L_Motor, R_Motor)
    # clear
    GPIO.cleanup()

