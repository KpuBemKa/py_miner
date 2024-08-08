from pynput.keyboard import Key, KeyCode

# The key to start the mining loop
START_KEY = Key.f6
# The key to stop the mining loop
STOP_KEY = Key.f7

# Increase the mining distance by half a block only for the next pass
INCREASE_DISTANCE_KEY = KeyCode(char="]")
# Decrease the mining distance by half a block only for the next pass
DECREASE_DISTANCE_KEY = KeyCode(char="\\")
# Increase the mining distance by a block only for the next pass
X2_INCREASE_DISTANCE_KEY = KeyCode(char="[")
# Decrease the mining distance by a block only for the next pass
X2_DECREASE_DISTANCE_KEY = KeyCode(char="'")
# Cancel shifting down for the next pass
CLEANUP_RUN_KEY = KeyCode(char=".")
