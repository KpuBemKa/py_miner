import sys
import time
from pynput.keyboard import Key, KeyCode, Listener, Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from speed_lookup_table import SLOW_FLY_SPEEDS

FLY_SPEED = 10.8  # blocks per second
ACC_TIME = 1

keyboard = KeyboardController()
mouse = MouseController()


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


def get_speed_on_tick(tick: int) -> float:
    if tick > len(SLOW_FLY_SPEEDS):
        return 0.544444
    else:
        return SLOW_FLY_SPEEDS[tick]
    # if tick == 0:
    #     return 0
    # else:
    #     # got this function from a function approximation site
    #     return (56 + ((2.86 - 56) / (1 + ((tick) / (8)) ** (1.64)))) / 100


# def get_velocity_next_tick(current_tick_speed: float) -> float:
#     SLIPPERINESS_MULTIPLIER = 1.0  # 1.0 for airborne
#     MOVEMENT_MULTIPLIER = (
#         1.0 * 0.98
#     )  # 1.0 for walking (not sprinting); 0.98 facing completely forward

#     return (
#         current_tick_speed * SLIPPERINESS_MULTIPLIER * 0.91 + 0.02 * MOVEMENT_MULTIPLIER
#     )


def calc_time_to_reach_block(travel_distance: int) -> float:
    distance = 0
    tick = 1
    speed = 0

    while distance < travel_distance:
        speed = get_speed_on_tick(tick)
        distance += speed
        tick += 1

    print(speed)
    return tick / 20

    # match travel_distance:
    #     case 1:
    #         return 0.17

    #     case 2:
    #         return 0.35

    #     case 3:
    #         return 0.5

    #     case 4:
    #         return 0.6

    #     case 5:
    #         return 0.7

    #     case 6:
    #         return 0.825

    # # FLY_FRICTION = 0.05  # ice friction which is the same as flying
    # FLY_FRICTION = 0.546  # ice friction which is the same as flying
    # # ACCEL = 0.53
    # ACCEL = 0.098

    # distance = 0
    # velocity = 0
    # tick_counter = 0
    # while distance < travel_distance:
    #     velocity += ACCEL

    #     print(velocity)
    #     distance += velocity

    #     velocity = velocity * FLY_FRICTION

    #     tick_counter += 1

    # return tick_counter / 20

    # one minecraft tick is 1/20 of a second
    # ACCEL_DECAY = 0.003  # blocks/tick^3
    # INITIAL_ACCEL = 0.05  # blocks/tick^2
    # # ACCEL_DECAY = 0.0025  # blocks/tick^3
    # # ACCEL_DECAY = 0  # blocks/tick^3
    # # INITIAL_ACCEL = 0.08  # blocks/tick^2

    # accel = INITIAL_ACCEL
    # speed = 0
    # tick_counter = 0
    # distance = 0

    # while distance <= travel_distance:
    #     speed += accel

    #     if accel > 0:
    #         accel -= ACCEL_DECAY
    #     else:
    #         accel = 0
    #     # accel -= ACCEL_DECAY

    #     # print(accel)

    #     # print(speed)
    #     distance += speed
    #     tick_counter += 1

    # print(speed)
    # return tick_counter / 20.0


def fly_blocks(amount: int) -> None:
    TIME_TO_STOP = 7/20
    
    time_to_sleep = calc_time_to_reach_block(amount) - TIME_TO_STOP
    # time_to_sleep = calc_time_to_reach_block(amount)
    print(time_to_sleep)

    # type_command("home")
    type_command("tp cverti 0.5 -59.5 0.5 180 90")

    time.sleep(2)

    keyboard.press("w")

    efficient_sleep(time_to_sleep)

    # keyboard.press(Key.esc)
    # time.sleep(1)
    # keyboard.press(Key.esc)
    
    keyboard.release("w")
    keyboard.press("s")
    efficient_sleep(TIME_TO_STOP)

    # keyboard.press(Key.esc)
    # time.sleep(1)
    # keyboard.press(Key.esc)
    
    keyboard.release("s")
    # slow_keyboard_tap(Key.shift_l)
    
    time.sleep(1)

    # slow_keyboard_tap(Key.space)
    # time.sleep(0.1)
    # slow_keyboard_tap(Key.space)


def execute_cycle(cycle_len: int) -> None:
    type_command("sethome")

    for _ in range(1, cycle_len + 1):
        fly_blocks()


def start_test():
    for i in range(1, 7):
        print(f"Testing for: {i}")
        for _ in range(0, 3):
            fly_blocks(10 * i)
            # fly_blocks(i)


def test_specific(blocks):
    while True:
        fly_blocks(blocks)


def main():
    if len(sys.argv) == 2:
        line_length = int(sys.argv[1])
    else:
        line_length = None

    def key_press_listener(key: KeyCode | Key):
        if key == Key.f8:
            if line_length:
                test_specific(line_length)
            else:
                start_test()

    listener = Listener(on_press=key_press_listener)
    listener.start()

    while True:
        time.sleep(1)


# main()

# for i in range(1, 6):
#     calc_time_to_reach_block(i)
#     print("------")

print(calc_time_to_reach_block(30))