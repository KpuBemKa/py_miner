import sys
import time
import traceback

from pynput.keyboard import Key, KeyCode, Listener, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from settings import START_KEY, STOP_KEY, HOME_N_RESTART_KEY

# RESTART_KEY = KeyCode(char="`")


mouse = MouseController()
keyboard = KeyboardController()


def main():
    reverse = False
    
    try:
        if len(sys.argv) == 2:
            reverse = True

        def key_press_listener(key: KeyCode | Key):
            if key == START_KEY:
                print("Miner started.")
                mouse.press(Button.left)

            elif key == STOP_KEY:
                print("Miner stopped.")
                mouse.release(Button.left)

            elif key == HOME_N_RESTART_KEY:
                keyboard.release(Key.space)
                mouse.release(Button.left)
                keyboard.tap("/")
                time.sleep(0.1)
                keyboard.type("home")
                keyboard.tap(Key.enter)
                
                if not reverse:
                    time.sleep(0.2)
                    mouse.press(Button.left)
            
            elif key == Key.tab:
                if not reverse:
                    return
                
                time.sleep(0.1)
                mouse.press(Button.left)
                # keyboard.press(Key.space)
                # time.sleep(50/1000)
                # keyboard.release(Key.space)
                # time.sleep(50/1000)
                keyboard.press(Key.space)
                    

        listener = Listener(on_press=key_press_listener)
        listener.start()

        print("Ready")

        while True:
            time.sleep(1)

    except Exception as ex:
        print(
            f"Exception during data reading: {ex.args}\n{ex}\n{traceback.format_exc()}"
        )


main()
