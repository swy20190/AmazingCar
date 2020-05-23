#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from math import pi
import time

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)

    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)


def forward(speed, duration, l_m, r_m):
    l_m.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)

    r_m.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)

    time.sleep(duration)


def backward(speed, duration, l_m, r_m):
    l_m.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)
    GPIO.output(AIN1, False)

    r_m.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)
    GPIO.output(BIN1, False)

    time.sleep(duration)


def brake(duration, l_m, r_m):
    l_m.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, False)

    r_m.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, False)

    time.sleep(duration)


# 差速转向
def turn(l_speed, r_speed, duration, l_m, r_m):
    l_m.ChangeDutyCycle(l_speed)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)

    r_m.ChangeDutyCycle(r_speed)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)

    time.sleep(duration)


# 半径为1米的转向
def advanced_turn(direction, duration, l_m, r_m):
    # 外侧轮转速
    faster_speed = 94.102
    # 内侧轮转速
    slower_speed = 80.0
    # 0为向左，1为向右
    if direction == 0:
        turn(l_speed=slower_speed, r_speed=faster_speed, duration=duration, l_m=l_m, r_m=r_m)
    else:
        turn(l_speed=faster_speed, r_speed=slower_speed, duration=duration, l_m=l_m, r_m=r_m)


# first, we must test the speed of the car
if __name__ == '__main__':
    init()
    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)
    # forward 1 meter
    # R = 65mm
    time_ward = 1.0  # 990.0/(90 / 48 * pi * 65)  # 由于惯性提前刹车，48是齿轮减速比
    forward(speed=90, duration=time_ward, l_m=L_Motor, r_m=R_Motor)
    # 1st brake
    brake(2.0, L_Motor, R_Motor)
    # backward 1 meter
    backward(90, time_ward, L_Motor, R_Motor)
    # 2nd brake
    brake(2.0, L_Motor, R_Motor)
    # turn left by 135 degree
    # speed of car
    turning_time = 0.5  # 0.75 * 1000 / (87.006 / 48 * 65)  # 不到7秒
    advanced_turn(direction=0, duration=turning_time, l_m=L_Motor, r_m=R_Motor)
    # 3rd brake
    brake(2.0, L_Motor, R_Motor)
    # turn right by 135 degree
    advanced_turn(direction=1, duration=turning_time, l_m=L_Motor, r_m=R_Motor)
    # 4nd brake
    brake(2.0, L_Motor, R_Motor)
    # clear
    GPIO.cleanup()

