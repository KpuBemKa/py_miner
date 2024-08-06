import time
import sys
import traceback

from pynput.keyboard import Key, KeyCode, Listener

from miner import Miner

from settings import START_KEY, STOP_KEY





def print_help():
    print("Usage: `python ./main.py <amount of block per line>`")


def main():
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print_help()
        return

    try:
        line_length = int(sys.argv[1])
        miner = Miner(line_length)

        def key_press_listener(key: KeyCode | Key):
            if key == START_KEY:
                print("Miner started.")
                miner.start()
            elif key == STOP_KEY:
                print("Miner stopped.")
                miner.stop()

        listener = Listener(on_press=key_press_listener)
        listener.start()

        print(f"Ready to mine {line_length} block per line.")
        
        while True:
            time.sleep(1)
    except ValueError:
        print("Error. Are you sure the first argument is an integer?")
    except Exception as ex:
        print(
            f"Exception during data reading: {ex.args}\n{ex}\n{traceback.format_exc()}"
        )


main()
