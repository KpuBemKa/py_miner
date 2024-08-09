import time
import threading
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button


TIME_TO_STOP = 7 / 20  # 7 ticks
STOP_DISTANCE = 2  # blocks

BASE_ACCEL = 0.049
FRICTION = 0.91

MAX_SPEED_BLOCK_TRAVEL_TIME = 0.092  # seconds per bock


class TerminateMiningException(Exception):
    """Should be raised to propagate the stack, and reach the mining infinite loop to cancel it

    Args:
        Exception (Exception): Some string with some text
    """


class SlowMiner:
    """Line miner without using regular fly (the one without Ctrl key)"""

    __keyboard: KeyboardController = KeyboardController()
    __mouse = MouseController()

    def __init__(self) -> None:
        self.__line_length: float = 0

        self.__fly_time_tweak: float = 0.0
        self.__ignore_shift_down: bool = False

        self.__mining_thread: threading.Thread | None = None
        self.__terminate_mining_flag = False

    def start_mining(self, line_length: float) -> None:
        """
        Resets its internal flags,
        and starts a thread with an infinte mining loop,
        which can be stopped using `stop_mining()`

        Args:
            line_length (float): Size of the line which sould be mined
        """
        if self.__mining_thread is not None:
            return

        self.__line_length = line_length
        self.__terminate_mining_flag = False

        self.__mining_thread = threading.Thread(
            target=self.__mining_executor, daemon=True
        )
        self.__mining_thread.start()

    def stop_mining(self) -> None:
        """Stops the infinte loop of mining started by `start_mining()`"""
        self.__set_terminate_mining_flag()

        self.__mouse.release(Button.left)
        self.__keyboard.release("w")
        self.__keyboard.release("s")
        self.__keyboard.release(Key.space)
        self.__keyboard.release(Key.shift)

        self.__mining_thread.join()
        self.__mining_thread = None

    def tweak_mining_distance(self, tweak_amount: float) -> None:
        """Changes the travel distance of the next flyby

        Args:
            tweak_amount (float):\
                Amount of blocks to change the distance.\
                Positive to increase the distance, negative to decrease it
        """
        self.__fly_time_tweak += tweak_amount * MAX_SPEED_BLOCK_TRAVEL_TIME

    def ignore_one_shift_down(self) -> None:
        """
        Makes so the next flyby will be started without shifting the player down.
        Useful for when a lot of pillars are accumulated on the line, which may impend the player
        """
        self.__ignore_shift_down = True

    def __mining_executor(self) -> None:
        try:
            self.__slow_keyboard_tap(Key.space, delay=50 / 1000)
            self.__accurate_sleep(50 / 1000)
            self.__slow_keyboard_tap(Key.space, delay=50 / 1000)
            self.__slow_keyboard_tap(Key.space, delay=100 / 1000)

            self.__mouse.press(Button.left)

            while True:
                self.__fly_forward()
                self.__shift_player_down()
                self.__fly_backward()
                self.__shift_player_down()

                # self.__type_command("repair")
                # self.__accurate_sleep(200 / 1000)
                # self.__mouse.press(Button.left)

        except TerminateMiningException:
            pass

    def __fly_forward(self) -> None:
        self.__fly_blocks(
            amount=self.__line_length,
            forward_key=KeyCode(char="w"),
            backward_key=KeyCode(char="s"),
        )

    def __fly_backward(self) -> None:
        self.__fly_blocks(
            amount=self.__line_length,
            forward_key=KeyCode(char="s"),
            backward_key=KeyCode(char="w"),
        )

    def __fly_blocks(
        self, amount: int, forward_key: KeyCode, backward_key: KeyCode
    ) -> None:
        self.__check_for_terminate_mining()

        # print(f"f:{forward_key}; b:{backward_key}; a{amount}")

        time_to_fly = self.__calc_time_to_reach_block(amount - STOP_DISTANCE)
        # self.__distance_tweak = 0
        # print(f"fly: {time_to_fly}; stop time: {TIME_TO_STOP}")

        # type_command("home")
        # type_command("tp cverti 0 -59.5 0 180 90")
        # type_command("tp cverti 0.5 -60 0 -90 90")

        # time.sleep(2)

        self.__keyboard.press(forward_key)
        self.__accurate_sleep(time_to_fly)
        self.__keyboard.release(forward_key)

        self.__keyboard.press(backward_key)
        self.__accurate_sleep(TIME_TO_STOP)
        self.__keyboard.release(backward_key)

        # self.__check_for_distance_tweak()

    # def __check_for_distance_tweak(self):
    #     if self.__distance_tweak == 0.0:
    #         return

    #     self.__keyboard.release("w")
    #     self.__keyboard.release("s")
    #     self.__accurate_sleep(300 / 1000)

    #     amount = abs(self.__distance_tweak)
    #     forward_key = "w" if self.__distance_tweak > 0 else "s"
    #     backward_key = "s" if self.__distance_tweak > 0 else "w"

    #     print(self.__distance_tweak)
    #     print(f"{forward_key} {backward_key}")

    #     self.__distance_tweak = 0

    #     self.__fly_blocks(amount, forward_key, backward_key)

    #     time.sleep(1)

    def __shift_player_down(self) -> None:
        if self.__ignore_shift_down:
            self.__ignore_shift_down = False
            self.__accurate_sleep(100 / 1000)
            return

        self.__slow_keyboard_tap(Key.shift_l, delay=150 / 1000)

    def __set_terminate_mining_flag(self) -> None:
        self.__terminate_mining_flag = True

    def __check_for_terminate_mining(self) -> None:
        if self.__terminate_mining_flag:
            self.__terminate_mining_flag = False
            raise TerminateMiningException("The flag to terminate mining was set.")

    def __calc_time_to_reach_block(self, distance: int) -> float:
        speed: float = 0
        traveled_distance: float = 0.0
        tick_count: int = 0

        while traveled_distance < distance:
            speed += BASE_ACCEL
            traveled_distance += speed
            speed *= FRICTION
            tick_count += 1

        return tick_count / 20

    def __slow_keyboard_tap(self, key: KeyCode, delay: float = 0.1) -> None:
        self.__keyboard.press(key)
        self.__accurate_sleep(delay)
        self.__keyboard.release(key)

    def __type_command(self, command: str) -> None:
        self.__keyboard.tap("/")
        time.sleep(0.1)
        self.__keyboard.type(command)
        self.__keyboard.tap(Key.enter)

    def __accurate_sleep(self, secs: float, expected_inaccuracy: float = 0.5) -> None:
        start = time.perf_counter()
        end = secs + start

        # time_to_sleep = secs - expected_inaccuracy if secs > expected_inaccuracy else 0

        # time.sleep(time_to_sleep)
        while time.perf_counter() < end:
            if self.__fly_time_tweak != 0:
                end += self.__fly_time_tweak
                print(f"Changed by: {self.__fly_time_tweak}")
                self.__fly_time_tweak = 0
            continue
