import time

import win32com.client
import os

from pynput.keyboard import Key, Listener, GlobalHotKeys, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()

# change this as you need:
PLAYER_NAME = "cverti"
TO_MINE_LENGTH = 129  # blocks
FORWARD_TWEAK_KEY = ']'
BACKWARD_TWEAK_KEY = '\\'
DOUBLE_FORWARD_TWEAK_KEY = '['
DOUBLE_BACKWARD_TWEAK_KEY = '\''

# do not change this tho
FLY_SPEED = 10.8  # blocks per second
FAST_FLY_SPEED = 21.6  # blocks per second

SHIFT_TIME = 0.11  # seconds
TWEAK_TIME = 0.05

FORWARD_TIME = (TO_MINE_LENGTH) / FAST_FLY_SPEED + 0.23
BACKWARD_TIME = (TO_MINE_LENGTH) / FLY_SPEED + 0.27

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate("Excalibur-Craft " + PLAYER_NAME)

forward_tweak_time = 0
backward_tweak_time = 0


def main():
    listener = Listener(on_press=on_press)
    hotkey_listener = GlobalHotKeys({
        '<ctrl>+' + FORWARD_TWEAK_KEY: forward_tweak_pressed,
        '<ctrl>+' + BACKWARD_TWEAK_KEY: backward_tweak_pressed,
        '<ctrl>+' + DOUBLE_FORWARD_TWEAK_KEY: double_forward_tweak_pressed,
        '<ctrl>+' + DOUBLE_BACKWARD_TWEAK_KEY: double_backward_tweak_pressed
    })
    listener.start()
    hotkey_listener.start()

    align_player()
    start_mining()

    listener.join()
    hotkey_listener.join()


def forward_tweak_pressed():
    print("Will fly a bit forward")
    global forward_tweak_time
    forward_tweak_time = TWEAK_TIME


def backward_tweak_pressed():
    print("Will fly a bit backward")
    global backward_tweak_time
    backward_tweak_time = TWEAK_TIME


def double_forward_tweak_pressed():
    print("Will fly x2 a bit forward")
    global forward_tweak_time
    forward_tweak_time = TWEAK_TIME * 2


def double_backward_tweak_pressed():
    print("Will fly x2 a bit backward")
    global backward_tweak_time
    backward_tweak_time = TWEAK_TIME * 2


def tweak(key, time_to_move):
    keyboard.press(key)
    efficient_sleep(time_to_move)
    keyboard.release(key)


def tweak_both_directions():
    global forward_tweak_time
    if forward_tweak_time > 0:
        tweak('w', forward_tweak_time)
        forward_tweak_time = 0
        print("Flown a bit forward")

    global backward_tweak_time
    if backward_tweak_time > 0:
        tweak('s', backward_tweak_time)
        backward_tweak_time = 0
        print("Flown a bit backward")


def on_press(key):
    try:
        if key.char == FORWARD_TWEAK_KEY:
            forward_tweak_pressed()
            return

        if key.char == BACKWARD_TWEAK_KEY:
            backward_tweak_pressed()
            return
        
        if key.char == DOUBLE_FORWARD_TWEAK_KEY:
            double_forward_tweak_pressed()
            return

        if key.char == DOUBLE_BACKWARD_TWEAK_KEY:
            double_backward_tweak_pressed()
            return

    except AttributeError:
        if key is Key.f6:
            keyboard.release("w")
            keyboard.release("s")
            keyboard.release(Key.shift_l)
            keyboard.release(Key.ctrl_l)
            mouse.release(Button.left)
            os._exit(0)


def efficient_sleep(secs, expected_inaccuracy=0.5):  # for longer times
    start = time.perf_counter()
    end = secs + start

    time_to_sleep = secs if secs > expected_inaccuracy else 0

    time.sleep(time_to_sleep)
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
    time.sleep(0.2)
    keyboard.release(Key.space)


def forward_mine():
    tweak_both_directions()

    keyboard.press("w")
    keyboard.press(Key.ctrl_l)

    efficient_sleep(FORWARD_TIME)

    keyboard.release("w")
    keyboard.release(Key.ctrl_l)

    tweak_both_directions()

    keyboard.press('s')
    efficient_sleep(0.6)
    keyboard.release('s')


def backward_mine():
    tweak_both_directions()

    keyboard.press("s")

    efficient_sleep(BACKWARD_TIME)

    keyboard.release("s")

    tweak_both_directions()

    keyboard.press('w')
    efficient_sleep(0.4)
    keyboard.release('w')


def shift_down():
    keyboard.press(Key.shift_l)

    time.sleep(SHIFT_TIME)

    keyboard.release(Key.shift_l)


def start_mining():
    while True:
        # loop_start = time.perf_counter()

        mouse.press(Button.left)

        forward_mine()
        shift_down()
        backward_mine()
        shift_down()
        # break

        # print("loop time: ", time.perf_counter() - loop_start)


main()
