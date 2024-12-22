from math import sqrt
import traceback
import keyboard
import time
import pyautogui
from PIL import Image

SAMPLE_POSITION = {
    'left': [(500, 595), (487, 609), (482, 618), (466, 642)],
    'middle': [(800, 596), (800, 608), (800, 622), (800, 645)],
    'right': [(1100, 596), (1109, 608), (1121, 612), (1132, 641)]
}
MAX_LOOP_TIME = 0.01
TARGET_COLOR = (252, 252, 252)
COLOR_COMPARE_THREADHOLD = 50


def calculate_threadhold(color_rgb: list):
    """Calculate distance between two pixel"""
    return sqrt(
        pow(color_rgb[0] - TARGET_COLOR[0], 2) +
        pow(color_rgb[1] - TARGET_COLOR[1], 2) +
        pow(color_rgb[2] - TARGET_COLOR[2], 2)
    )


def is_found(screenshot: Image, positions: list):
    """Check if found the target in set positions"""
    for position in positions:
        pixel = screenshot.getpixel(position)
        pixel_threadhold = calculate_threadhold(pixel)
        if pixel_threadhold < COLOR_COMPARE_THREADHOLD:
            return True
    return False


def take_screenshot():
    """Take screenshot and check the position"""
    screenshot = pyautogui.screenshot()

    check_result = is_found(screenshot, SAMPLE_POSITION['left'])
    if check_result:
        return 'left'

    check_result = is_found(screenshot, SAMPLE_POSITION['middle'])
    if check_result:
        return 'middle'

    check_result = is_found(screenshot, SAMPLE_POSITION['right'])
    if check_result:
        return 'right'

    return ''


def click_target(name: str):
    """Press and release the A, S or D key"""

    # DEBUG
    print('[CLICK_TARGET] ', 'A' if name == 'left' else 'S' if name == 'middle' else 'D' if name == 'right' else '')

    # Press key
    if name == 'left':
        keyboard.press_and_release('a')
        return
    if name == 'middle':
        keyboard.press_and_release('s')
        return
    if name == 'right':
        keyboard.press_and_release('d')
        return


if __name__ == '__main__':
    print('[START]')

    is_active = False

    while True:
        try:
            start_tsms = time.perf_counter()

            # Hanle keyboard press
            if keyboard.is_pressed('F1'):
                print('[Keypress] Exit ...')
                break
            elif keyboard.is_pressed('F2'):
                is_active = not is_active
                print(f'[Keypress] Toggle script {is_active=}')
                time.sleep(0.5)  # Stop a bit for not toggle again

            # When script active
            if is_active:
                click_target_name = take_screenshot()
                if click_target_name:
                    print(f'==============> {click_target_name=}')
                    click_target(click_target_name)
                    if click_target_name:
                        time.sleep(0.075)  # Stop a bit for the disappear animation

            # Wait until enough loop time
            end_tsms = time.perf_counter()
            run_time = end_tsms - start_tsms
            if run_time < MAX_LOOP_TIME:
                time.sleep(MAX_LOOP_TIME - run_time)

        except Exception:
            traceback.print_exc()
            break

    print('[END]')
