import sys
import time
from pynput.keyboard import Key, KeyCode, Listener, Controller as KeyboardController

keyboard = KeyboardController()


FLY_SPEED = 10.8  # blocks per second
ACC_TIME = 1


def slow_keyboard_tap(key: KeyCode, delay: float = 0.1) -> None:
    keyboard.press(key)
    time.sleep(delay)
    keyboard.release(key)


def type_command(command: str) -> None:
    keyboard.tap("/")
    time.sleep(0.1)
    keyboard.type(command)
    keyboard.tap(Key.enter)


def efficient_sleep(secs: float):  # for longer times
    start = time.perf_counter()
    end = secs + start

    # time_to_sleep = secs if secs > expected_inaccuracy else 0

    # time.sleep(time_to_sleep)
    while time.perf_counter() < end:
        continue
    return


def calc_time_to_reach_block(distance: int) -> float:
    # one minecraft tick is 1/20 of a second
    ACCEL_DECAY = 0.003  # blocks/tick^3
    INITIAL_ACCEL = 0.05  # blocks/tick^2

    accel = INITIAL_ACCEL
    speed = 0
    tick_counter = 0

    while distance > 0:
        speed += accel
            
        if accel >= 0:
            accel -= ACCEL_DECAY

        print(speed)
        distance -= speed
        tick_counter += 1

    return tick_counter / 20


def fly_blocks(amount: int) -> None:
    time_to_sleep = calc_time_to_reach_block(amount)
    print(f"Time to sleep: {time_to_sleep}")

    type_command("home")

    time.sleep(2)

    keyboard.press("w")

    efficient_sleep(time_to_sleep)

    keyboard.release("w")

    slow_keyboard_tap(Key.shift_l)

    time.sleep(2)

    slow_keyboard_tap(Key.space)
    time.sleep(0.1)
    slow_keyboard_tap(Key.space)


def start_test(blocks: int):
    while True:
        fly_blocks(blocks)


def main():
    line_length = int(sys.argv[1])

    def key_press_listener(key: KeyCode | Key):
        if key == Key.f8:
            start_test(line_length)

    listener = Listener(on_press=key_press_listener)
    listener.start()

    while True:
        time.sleep(1)


main()
