import time
import traceback
import keyboard


MAX_LOOP_TIME = 0.01

if __name__ == '__main__':
    print('[START]')

    is_active = False

    while True:
        try:
            start_tsms = time.perf_counter()

            if keyboard.is_pressed('F1'):
                print('[Keypress] Exit ...')
                break
            elif keyboard.is_pressed('F2'):
                is_active = not is_active
                print(f'[Keypress] Toggle script {is_active=}')
                time.sleep(0.5)

            if is_active:
                keyboard.press_and_release('a')
                time.sleep(0.16666)
                keyboard.press_and_release('d')
                time.sleep(0.16666)

            end_tsms = time.perf_counter()
            run_time = end_tsms - start_tsms
            if run_time < MAX_LOOP_TIME:
                time.sleep(MAX_LOOP_TIME - run_time)

        except Exception:
            traceback.print_exc()
            break

    print('[END]')
