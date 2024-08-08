# import sys
# import time
# from pynput.keyboard import Key, KeyCode, Listener, Controller as KeyboardController
# from pynput.mouse import Controller as MouseController, Button
# from speed_lookup_table import SLOW_FLY_SPEEDS

# FLY_SPEED = 10.8  # blocks per second
# ACC_TIME = 1


# class SlowMiner:
#     __keyboard: KeyboardController = KeyboardController()
#     __mouse = MouseController()

#     def __init__(self) -> None:
#         pass
    
#     def fly_blocks(amount: int) -> None:
#         TIME_TO_STOP = 7 / 20
#         STOP_DISTANCE = 2

#         time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - STOP_DISTANCE)
#         # time_to_stop, distance_to_stop = calc_time_to_stop(end_speed)
#         # time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - distance_to_stop)
#         # time_to_stop = TIME_TO_STOP
#         # time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - distance_to_stop)
#         # time_to_sleep = calc_time_to_reach_block(amount)
#         print(f"fly: {time_to_fly}; stop time: {TIME_TO_STOP}")

#         type_command("home")
#         # type_command("tp cverti 0 -59.5 0 180 90")
#         # type_command("tp cverti 0.5 -60 0 -90 90")

#         time.sleep(2)

#         keyboard.press("w")

#         efficient_sleep(time_to_fly)

#         # keyboard.press(Key.esc)
#         # time.sleep(1)
#         # keyboard.press(Key.esc)

#         keyboard.release("w")

#         keyboard.press("s")
#         efficient_sleep(TIME_TO_STOP)
#         keyboard.release("s")

#         time.sleep(1)

#     def __calc_time_to_reach_block(distance: int) -> float:
#         BASE_ACCEL = 0.049
#         FRICTION = 0.91

#         speed: float = 0
#         traveled_distance: float = 0.0
#         tick_count: int = 0

#         while traveled_distance < distance:
#             speed += BASE_ACCEL
#             traveled_distance += speed
#             speed *= FRICTION
#             tick_count += 1

#         return tick_count / 20

#     def __slow_keyboard_tap(self, key: KeyCode, delay: float = 0.1) -> None:
#         self.__keyboard.press(key)
#         time.sleep(delay)
#         self.__keyboard.release(key)

#     def __efficient_sleep(secs: float, expected_inaccuracy: float = 0.5) -> None:
#         start = time.perf_counter()
#         end = secs + start

#         time_to_sleep = secs - expected_inaccuracy if secs > expected_inaccuracy else 0

#         time.sleep(time_to_sleep)
#         while time.perf_counter() < end:
#             continue
#         return


# # def type_command(command: str) -> None:
# #     keyboard.tap("/")
# #     time.sleep(0.1)
# #     keyboard.type(command)
# #     keyboard.tap(Key.enter)


# # def get_speed_on_tick(tick: int) -> float:
# #     if tick > len(SLOW_FLY_SPEEDS):
# #         return 0.544444
# #     else:
# #         return SLOW_FLY_SPEEDS[tick]
# #     # if tick == 0:
# #     #     return 0
# #     # else:
# #     #     # got this function from a function approximation site
# #     #     return (56 + ((2.86 - 56) / (1 + ((tick) / (8)) ** (1.64)))) / 100


# # def get_velocity_next_tick(current_tick_speed: float) -> float:
# #     SLIPPERINESS_MULTIPLIER = 1.0  # 1.0 for airborne
# #     MOVEMENT_MULTIPLIER = (
# #         1.0 * 0.98
# #     )  # 1.0 for walking (not sprinting); 0.98 facing completely forward

# #     return (
# #         current_tick_speed * SLIPPERINESS_MULTIPLIER * 0.91 + 0.02 * MOVEMENT_MULTIPLIER
# #     )


# # def calc_time_to_stop(speed: float) -> tuple[float, float]:
# #     """_summary_

# #     Args:
# #         speed (float): _description_

# #     Returns:
# #         tuple[float, float]: [time to stop; distance traveled while stopping]
# #     """
# #     BASE_ACCEL = 0.049
# #     FRICTION = 0.91

# #     speed: float = abs(speed)
# #     distance: float = 0.0
# #     tick_count: int = 0

# #     while speed > abs(0.0166):
# #         speed += -BASE_ACCEL
# #         distance += speed
# #         # print(speed)
# #         speed *= FRICTION
# #         tick_count += 1

# #     # if speed >= abs(0.0166)
# #     return tuple([tick_count / 20, distance])


# def calc_time_to_reach_block(start_speed: float, distance: int) -> float:
#     """_summary_

#     Args:
#         start_speed (float): _description_
#         distance (int): _description_

#     Returns:
#         float: _description_
#     """
#     BASE_ACCEL = 0.049
#     FRICTION = 0.91

#     speed: float = start_speed
#     traveled_distance: float = 0.0
#     tick_count: int = 0

#     while traveled_distance < distance:
#         speed += BASE_ACCEL
#         # print(speed)
#         traveled_distance += speed
#         speed *= FRICTION
#         tick_count += 1

#     # return tuple([tick_count / 20, speed])
#     return tick_count / 20

#     # distance = 0
#     # tick = 1
#     # speed = 0

#     # while distance < travel_distance:
#     #     speed = get_speed_on_tick(tick)
#     #     distance += speed
#     #     tick += 1

#     # print(speed)
#     # return tick / 20


# def stop_to_zero():
#     MAX_SPEED = 0.5444

#     time_to_sleep, distance = calc_time_to_stop(MAX_SPEED)

#     keyboard.press("w")
#     time.sleep(5)
#     keyboard.release("w")

#     keyboard.press("s")
#     efficient_sleep(time_to_sleep)
#     keyboard.release("s")


# def fly_blocks(amount: int) -> None:
#     TIME_TO_STOP = 7 / 20
#     STOP_DISTANCE = 2

#     time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - STOP_DISTANCE)
#     # time_to_stop, distance_to_stop = calc_time_to_stop(end_speed)
#     # time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - distance_to_stop)
#     # time_to_stop = TIME_TO_STOP
#     # time_to_fly, end_speed = calc_time_to_reach_block(0.0, amount - distance_to_stop)
#     # time_to_sleep = calc_time_to_reach_block(amount)
#     print(f"fly: {time_to_fly}; stop time: {TIME_TO_STOP}")

#     type_command("home")
#     # type_command("tp cverti 0 -59.5 0 180 90")
#     # type_command("tp cverti 0.5 -60 0 -90 90")

#     time.sleep(2)

#     keyboard.press("w")

#     efficient_sleep(time_to_fly)

#     # keyboard.press(Key.esc)
#     # time.sleep(1)
#     # keyboard.press(Key.esc)

#     keyboard.release("w")

#     keyboard.press("s")
#     efficient_sleep(TIME_TO_STOP)
#     keyboard.release("s")

#     time.sleep(1)


# def execute_cycle(cycle_len: int) -> None:
#     type_command("sethome")

#     for _ in range(1, cycle_len + 1):
#         fly_blocks()


# def start_test():
#     for i in range(3, 7):
#         print(f"Testing for: {i}")
#         for _ in range(0, 5):
#             fly_blocks(10 * i)
#             # fly_blocks(i)


# def test_specific(blocks):
#     while True:
#         fly_blocks(blocks)


# def main():
#     if len(sys.argv) == 2:
#         line_length = int(sys.argv[1])
#     else:
#         line_length = None

#     def key_press_listener(key: KeyCode | Key):
#         if key == Key.f8:
#             if line_length:
#                 test_specific(line_length)
#             else:
#                 start_test()
#         elif key == Key.f9:
#             stop_to_zero()

#     listener = Listener(on_press=key_press_listener)
#     listener.start()

#     while True:
#         time.sleep(1)


# # def test_vel():
# #     ACCEL = 0.049
# #     # ACCEL = 0
# #     FRICTION = 0.91

# #     speed = 0.544400783532487
# #     for _ in range(0, 100):
# #         speed += -ACCEL
# #         print(speed)
# #         speed *= FRICTION


# main()

# # for i in range(1, 6):
# #     calc_time_to_reach_block(i)
# #     print("------")

# # test_vel()

# # print(calc_time_to_reach_block(30))
