import threading
import time

from pynput.keyboard import (
    Key,
    KeyCode,
    Listener,
    Controller as KeyboardController,
)
from pynput.mouse import Button, Controller as MouseController

from settings import (
    FORWARD_TWEAK_KEY,
    BACKWARD_TWEAK_KEY,
    DOUBLE_FORWARD_TWEAK_KEY,
    DOUBLE_BACKWARD_TWEAK_KEY,
    CLEANUP_RUN_KEY,
)


FLY_SPEED = 10.8  # blocks per second
FAST_FLY_SPEED = 21.6  # blocks per second

SHIFT_TIME = 0.11  # seconds
TWEAK_TIME = 0.05


class StopThreadException(Exception):
    pass


class Miner:
    def __init__(self, line_length: int) -> None:
        self.__keyboard = KeyboardController()
        self.__mouse = MouseController()

        self.__forward_time = (line_length) / FAST_FLY_SPEED + 0.23
        self.__backward_time = (line_length) / FLY_SPEED + 0.2675

        self.__forward_tweak_time = 0
        self.__backward_tweak_time = 0
        self.__cleanup_flag = False

        self.__listener = Listener(on_press=self.__on_press_listner)
        self.__listener.start()

        self.__stop_mining_flag = False
        self.__miner_thread = None

    def start(self):
        if self.__miner_thread is not None:
            return

        self.__miner_thread = threading.Thread(
            target=self.__miner_executor, daemon=True
        )
        self.__miner_thread.start()

    def stop(self):
        if self.__miner_thread is None:
            return
        
        self.__listener.stop()

        self.__keyboard.release("w")
        self.__keyboard.release("s")
        self.__keyboard.press(Key.shift_l)
        self.__keyboard.release(Key.shift_l)
        self.__keyboard.release(Key.ctrl_l)
        self.__mouse.release(Button.left)
        
        # set a flag to stop miner thread and wait
        self.__stop_mining_flag = True
        self.__miner_thread.join()
        self.__miner_thread = None

    def __miner_executor(self):
        self.__raise_player()

        while True:
            try:
                self.__mine_one_pass()
            except StopThreadException:
                return

    def __mine_one_pass(self):
        self.__mouse.press(Button.left)

        self.__forward_mine()
        self.__shift_down()
        self.__backward_mine()
        self.__shift_down()

    def __forward_mine(self):
        self.__tweak_both_directions()

        self.__keyboard.press("w")
        self.__keyboard.press(Key.ctrl_l)

        self.__efficient_sleep(self.__forward_time)

        self.__keyboard.release("w")
        self.__keyboard.release(Key.ctrl_l)

        self.__tweak_both_directions()

        self.__keyboard.press("s")
        self.__efficient_sleep(0.6)
        self.__keyboard.release("s")

    def __backward_mine(self):
        self.__tweak_both_directions()

        self.__keyboard.press("s")

        self.__efficient_sleep(self.__backward_time)

        self.__keyboard.release("s")

        self.__tweak_both_directions()

        self.__keyboard.press("w")
        self.__efficient_sleep(0.4)
        self.__keyboard.release("w")

    def __shift_down(self):
        # if cleanup flag is set, shift down should not be executed
        if self.__cleanup_flag:
            self.__cleanup_flag = False
            return

        self.__keyboard.press(Key.shift_l)

        time.sleep(SHIFT_TIME)

        self.__keyboard.release(Key.shift_l)

    def __tweak_both_directions(self):
        if self.__should_mining_be_stopped():
            raise StopThreadException("Mining should be stopped.")
        
        if self.__forward_tweak_time > 0:
            self.__press_release_key("w", self.__forward_tweak_time)
            self.__forward_tweak_time = 0
            print("Flown a bit forward.")

        if self.__backward_tweak_time > 0:
            self.__press_release_key("s", self.__backward_tweak_time)
            self.__backward_tweak_time = 0
            print("Flown a bit backward.")

    def __press_release_key(self, key: str, delay: float):
        self.__keyboard.press(key)
        self.__efficient_sleep(delay)
        self.__keyboard.release(key)

    def __raise_player(self):
        # pynput tap() is too fast

        self.__keyboard.press(Key.space)
        time.sleep(0.05)
        self.__keyboard.release(Key.space)
        time.sleep(0.05)
        self.__keyboard.press(Key.space)
        time.sleep(0.2)
        self.__keyboard.release(Key.space)
        
    def __should_mining_be_stopped(self) -> bool:
        return self.__stop_mining_flag

    def __on_press_listner(self, key: KeyCode):
        try:
            if key.char == FORWARD_TWEAK_KEY:
                self.__forward_tweak_pressed()

            elif key.char == BACKWARD_TWEAK_KEY:
                self.__backward_tweak_pressed()

            elif key.char == DOUBLE_FORWARD_TWEAK_KEY:
                self.__double_forward_tweak_pressed()

            elif key.char == DOUBLE_BACKWARD_TWEAK_KEY:
                self.__double_backward_tweak_pressed()

            elif key.char == CLEANUP_RUN_KEY:
                self.__cleanup_pressed()
        except AttributeError:
            pass

    def __cleanup_pressed(self) -> None:
        print("Next flyby will be a cleanup one.")
        self.__cleanup_flag = True

    def __forward_tweak_pressed(self) -> None:
        print("This flyby will be a bit more forward.")
        self.__forward_tweak_time = TWEAK_TIME

    def __backward_tweak_pressed(self) -> None:
        print("This flyby will be a bit more backward.")
        self.__backward_tweak_time = TWEAK_TIME

    def __double_forward_tweak_pressed(self):
        print("This flyby will be more forward.")
        self.__forward_tweak_time = TWEAK_TIME * 2

    def __double_backward_tweak_pressed(self):
        print("This flyby will be more backward")
        self.__backward_tweak_time = TWEAK_TIME * 2

    def __efficient_sleep(self, secs, expected_inaccuracy=0.5):  # for longer times
        start = time.perf_counter()
        end = secs + start

        time_to_sleep = secs if secs > expected_inaccuracy else 0

        time.sleep(time_to_sleep)
        while time.perf_counter() < end:
            continue
        return start, time.perf_counter()
