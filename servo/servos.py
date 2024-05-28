import time
from typing import Iterable

import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = board.I2C()

pca = PCA9685(i2c)

pca.frequency = 50

servos = [servo.Servo(pca.channels[n]) for n in list(range(0,4))+list(range(14,16))]
angles = [0 for _ in range(0,6)]

PULLED_BACK_POS = 0
FULLY_DISPENSED_POS = 145
REST_POS = 100

SPEED_SLOW = 350
SPEED_FAST = 150

def a_to_b(a:int,b:int) -> Iterable[int]:
    """Returns every number from A to B"""
    return range(a,b) if b > a else range(a,b,-1)

def move_to(servo_id, angle:int, speed=SPEED_SLOW):
    servo = servos[servo_id]
    start_angle = angles[servo_id]
    print(f"Moving from {servo.angle} to {angle}")
    for angle in a_to_b(start_angle, angle):
        servo.angle = angle
        angles[servo_id] = angle
        time.sleep(1/speed)

def dispense(servo_id:int):
    time.sleep(0.1)
    move_to(servo_id, PULLED_BACK_POS)
    time.sleep(0.1)
    move_to(servo_id, FULLY_DISPENSED_POS, speed=SPEED_SLOW)
    time.sleep(0.1)
    move_to(servo_id, REST_POS)
    time.sleep(0.5)
    servo.angle = None

def unlock(servo_id:int):
    """ Moves a servo to the PULLED_BACK_POS and disables the motor."""
    move_to(servo_id, PULLED_BACK_POS)
    time.sleep(0.5)
    # Setting to None disables the motor.
    servos[servo_id].angle = None

def main():
    for i in range(50):
        dispense(3)
    time.sleep(9999)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        for servo in servos:
            servo.angle = None
        pca.deinit()
