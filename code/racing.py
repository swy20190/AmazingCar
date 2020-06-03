#!/usr/bin/python
# -*- coding: utf-8 -*-
# 直线竞速，干就vans了
import RPi.GPIO as GPIO
import time

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

max_velocity = 122  # 具体数据待测


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(PWMA, GPIO.OUT)

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


# 稍微向左调整，修正轮子的误差（真坑
def short_left(l_m, r_m):
    l_m.ChangeDutyCycle(0)
    r_m.ChangeDutyCycle(100)
    time.sleep(0.2)


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


if __name__ == '__main__':
    init()
    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)
    # forward_time = 380 / max_velocity
    forward(100.0, 3, L_Motor, R_Motor)
    short_left(L_Motor, R_Motor)
    forward(100.0, 2, L_Motor, R_Motor)
    brake(0.05, L_Motor, R_Motor)

    backward(95, 0.01, L_Motor, R_Motor)
    GPIO.cleanup()

