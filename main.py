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
BLOCKS_CONSTANT = 10  # acoounts for acceleration from 0 b/s
FLY_SPEED = 10.8  # blocks per second
FAST_FLY_SPEED = 21.6 # blocks per second
SHIFT_TIME = 0.13  # seconds

FORWARD_TIME = (TO_MINE_LENGTH  + BLOCKS_CONSTANT) / FAST_FLY_SPEED - SHIFT_TIME
BACKWARD_TIME = (TO_MINE_LENGTH  + BLOCKS_CONSTANT) / FLY_SPEED - SHIFT_TIME

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate("Excalibur-Craft " + PLAYER_NAME)

keyboard = KeyboardController()
mouse = MouseController()

def align_player():    
    keyboard.press(Key.space)
    time.sleep(0.05)
    keyboard.release(Key.space)
    time.sleep(0.05)
    keyboard.press(Key.space)
    time.sleep(0.15)
    keyboard.release(Key.space)
    
    keyboard.press('s')
    time.sleep(0.15)
    keyboard.release('s')
    keyboard.press('w')
    time.sleep(0.05)
    keyboard.release('w')

def start_mining():
    mouse.press(Button.left)
    keyboard.press(Key.ctrl_l)

    # first time launch
    keyboard.press("w")
    time.sleep(FORWARD_TIME) 
    keyboard.release("w")

    while not win32api.GetKeyState(win32con.VK_F6):
        keyboard.press("s")
        keyboard.press(Key.shift_l)
        time.sleep(SHIFT_TIME)
        keyboard.release(Key.shift_l)
        time.sleep(BACKWARD_TIME)
        keyboard.release("s")

        keyboard.press("w")
        keyboard.press(Key.shift_l)
        time.sleep(SHIFT_TIME)
        keyboard.release(Key.shift_l)
        time.sleep(FORWARD_TIME)
        keyboard.release("w")

    keyboard.release("w")
    keyboard.release("s")
    keyboard.release(Key.shift_l)
    keyboard.release(Key.ctrl_l)
    mouse.release(Button.left)
    time.sleep(0.1)


align_player()
start_mining()