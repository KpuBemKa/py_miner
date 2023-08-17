import win32com.client
import win32api
import win32con
import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# change this as you need:
PLAYER_NAME = "cverti"
TO_MINE_LENGTH = 55  # blocks

# do not change this tho
BLOCKS_CONSTANT = 8  # acoounts for acceleration from 0 b/s
FLY_SPEED = 10.8  # blocks per second
SHIFT_TIME = 0.13  # seconds

ONE_WAY_TIME = (TO_MINE_LENGTH  + BLOCKS_CONSTANT) / FLY_SPEED - SHIFT_TIME

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate("Excalibur-Craft " + PLAYER_NAME)

keyboard = KeyboardController()
mouse = MouseController()

mouse.press(Button.left)

# first time launch
keyboard.press("w")
time.sleep(ONE_WAY_TIME - SHIFT_TIME) 
keyboard.release("w")

while not win32api.GetKeyState(win32con.VK_F6):
    keyboard.press("s")
    keyboard.press(Key.shift)
    time.sleep(SHIFT_TIME)
    keyboard.release(Key.shift)
    time.sleep(ONE_WAY_TIME)
    keyboard.release("s")

    keyboard.press("w")
    keyboard.press(Key.shift)
    time.sleep(SHIFT_TIME)
    keyboard.release(Key.shift)
    time.sleep(ONE_WAY_TIME)
    keyboard.release("w")

keyboard.release("w")
keyboard.release("s")
mouse.release(Button.left)
time.sleep(0.1)
