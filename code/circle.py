#!/usr/bin/python
# -*- coding: utf-8 -*-
# 圆周避障
import RPi.GPIO as GPIO
import time

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

trigger = 20
echo = 21


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)

    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)

    GPIO.setup(trigger, GPIO.OUT, GPIO.LOW)
    GPIO.setup(echo, GPIO.IN)


def measure():
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(trigger, GPIO.LOW)

    while GPIO.input(echo) == 0:
        pass
    start = time.time()

    while GPIO.input(echo) == 1:
        pass
    end = time.time()

    return (end - start) * 343 / 2.0


# 差速转向
def turn(l_speed, r_speed, duration, l_m, r_m, forward):
    l_m.ChangeDutyCycle(l_speed)
    if forward:
        GPIO.output(AIN2, False)
        GPIO.output(AIN1, True)
    else:
        GPIO.output(AIN2, True)
        GPIO.output(AIN1, False)

    r_m.ChangeDutyCycle(r_speed)
    if forward:
        GPIO.output(BIN2, False)
        GPIO.output(BIN1, True)
    else:
        GPIO.output(BIN2, True)
        GPIO.output(BIN1, False)

    time.sleep(duration)


# 半径为1米的转向
def advanced_turn(direction, duration, l_m, r_m, forward):
    # 外侧轮转速
    faster_speed = 94.102
    # 内侧轮转速
    slower_speed = 80.0
    # 0为向左，1为向右
    if direction == 0:
        turn(l_speed=slower_speed, r_speed=faster_speed, duration=duration, l_m=l_m, r_m=r_m, forward=forward)
    else:
        turn(l_speed=faster_speed, r_speed=slower_speed, duration=duration, l_m=l_m, r_m=r_m, forward=forward)


def pivot_turn(direction, l_m, r_m, forward):
    pivot_time = 1.0  # 具体时间待测
    faster_speed = 80
    slower_speed = 0.0
    if direction == 0:
        turn(l_speed=slower_speed, r_speed=faster_speed,duration=pivot_time, l_m=l_m, r_m=r_m, forward=forward)
    else:
        turn(l_speed=faster_speed, r_speed=slower_speed, duration=pivot_time, l_m=l_m, r_m=r_m, forward=forward)


if __name__ == '__main__':
    init()
    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)
    # 首先原地右转90度
    pivot_turn(direction=1, l_m=L_Motor, r_m=R_Motor, forward=True)
