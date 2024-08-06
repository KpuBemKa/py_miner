import time
import traceback

from pynput.keyboard import Key, KeyCode, Listener
from pynput.mouse import Button, Controller as MouseController

from settings import START_KEY, STOP_KEY


mouse = MouseController()


def main():
    try:
        def key_press_listener(key: KeyCode | Key):
            if key == START_KEY:
                print("Miner started.")
                mouse.press(Button.left)
            elif key == STOP_KEY:
                print("Miner stopped.")
                mouse.release(Button.left)

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
