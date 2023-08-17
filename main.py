import time

import win32com.client
import win32api
import win32con

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# change this as you need:
PLAYER_NAME = "cverti"
TO_MINE_LENGTH = 55  # blocks

# do not change this tho
FLY_SPEED = 10.8  # blocks per second
FAST_FLY_SPEED = 21.6  # blocks per second
BLOCKS_CONSTANT = 10  # acoounts for acceleration from 0 b/s
SHIFT_TIME = 0.112  # seconds

FIRST_FORWARD_TIME = (TO_MINE_LENGTH + 5) / FAST_FLY_SPEED
FORWARD_TIME = (TO_MINE_LENGTH + BLOCKS_CONSTANT + 0.5) / FAST_FLY_SPEED - SHIFT_TIME
BACKWARD_TIME = (TO_MINE_LENGTH + BLOCKS_CONSTANT + 0.5) / FLY_SPEED - SHIFT_TIME

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate("Excalibur-Craft " + PLAYER_NAME)

keyboard = KeyboardController()
mouse = MouseController()


def efficient_sleep(secs, expected_inaccuracy=0.5):  # for longer times
    start = time.perf_counter()
    end = secs + start

    time.sleep(secs - expected_inaccuracy)
    while time.perf_counter() < end:
        continue
    return start, time.perf_counter()


def align_player():
    # tap() is too fast

    keyboard.press(Key.space)
    time.sleep(0.05)
    keyboard.release(Key.space)
    time.sleep(0.05)
    keyboard.press(Key.space)
    time.sleep(0.15)
    keyboard.release(Key.space)

    # keyboard.press('s')
    # event.wait(0.3)
    # keyboard.release('s')
    # keyboard.press('w')
    # event.wait(0.05)
    # keyboard.release('w')


def start_mining():
    mouse.press(Button.left)
    keyboard.press(Key.ctrl_l)

    # first time launch
    keyboard.press("w")
    efficient_sleep(FIRST_FORWARD_TIME)
    keyboard.release("w")

    keyboard.press("s")
    while not win32api.GetKeyState(win32con.VK_F6):
        keyboard.press(Key.ctrl_l)

        keyboard.press(Key.shift_l)
        time.sleep(SHIFT_TIME)
        keyboard.release(Key.shift_l)

        efficient_sleep(BACKWARD_TIME)

        keyboard.press("w")
        keyboard.release("s")

        keyboard.press(Key.shift_l)
        time.sleep(SHIFT_TIME)
        keyboard.release(Key.shift_l)
        efficient_sleep(FORWARD_TIME)

        keyboard.press("s")
        keyboard.release("w")

    keyboard.release("w")
    keyboard.release("s")
    keyboard.release(Key.shift_l)
    keyboard.release(Key.ctrl_l)
    mouse.release(Button.left)


align_player()
start_mining()
