import time
import sys

from pynput.keyboard import Key, KeyCode, Listener

# from miner import Miner
from slow_miner import SlowMiner

from settings import (
    START_KEY,
    STOP_KEY,
    INCREASE_DISTANCE_KEY,
    X2_INCREASE_DISTANCE_KEY,
    DECREASE_DISTANCE_KEY,
    X2_DECREASE_DISTANCE_KEY,
    CLEANUP_RUN_KEY,
)


def print_help():
    print("Usage: `python ./main.py <amount of block per line>`")


def main():
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print_help()
        return

    try:
        line_length = int(sys.argv[1])
        miner = SlowMiner()

        def key_press_listener(key: KeyCode | Key):
            if key == START_KEY:
                miner.start_mining(line_length)
                print("Miner started.")

            elif key == STOP_KEY:
                print("Stopping miner...")
                miner.stop_mining()
                print("Miner stopped.")

            elif key == INCREASE_DISTANCE_KEY:
                miner.tweak_mining_distance(0.5)
                print(f"This flyby distance is increased by {0.5} blocks")

            elif key == X2_INCREASE_DISTANCE_KEY:
                miner.tweak_mining_distance(1.0)
                print(f"This flyby distance is increased by {1} block")

            elif key == DECREASE_DISTANCE_KEY:
                miner.tweak_mining_distance(-0.5)
                print(f"This flyby distance is decreased by {0.5} blocks")

            elif key == X2_DECREASE_DISTANCE_KEY:
                miner.tweak_mining_distance(-1)
                print(f"This flyby distance is decreased by {1} block")

            elif key == CLEANUP_RUN_KEY:
                print("Next flyby will be a cleanup one")
                miner.ignore_one_shift_down()

        listener = Listener(on_press=key_press_listener)
        listener.start()

        print(f"Ready to mine {line_length} blocks per line.")

        while True:
            time.sleep(1)
    except ValueError:
        print("Error. Are you sure the first argument is an integer?")


main()
