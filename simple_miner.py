import time
import traceback

from pynput.keyboard import Key, KeyCode, Listener, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from settings import START_KEY, STOP_KEY

RESTART_KEY = Key.f8


mouse = MouseController()
keyboard = KeyboardController()


def main():
    try:

        def key_press_listener(key: KeyCode | Key):
            if key == START_KEY:
                print("Miner started.")
                mouse.press(Button.left)

            elif key == STOP_KEY:
                print("Miner stopped.")
                mouse.release(Button.left)

            elif key == RESTART_KEY:
                mouse.release(Button.left)
                keyboard.tap("/")
                time.sleep(0.1)
                keyboard.type("home")
                keyboard.tap(Key.enter)
                time.sleep(0.2)
                mouse.press(Button.left)

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
