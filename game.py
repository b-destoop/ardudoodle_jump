import serial
import pygame
import time

arduino = serial.Serial(port="COM15", baudrate=115200, timeout=0.01)
time.sleep(.01)
