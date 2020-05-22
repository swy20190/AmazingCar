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


