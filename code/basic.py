# this file contains basic functions of the car
import RPi.GPIO as GPIO
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


if __name__ == '__main__':
    init()
    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)

