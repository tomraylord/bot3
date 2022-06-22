from pywinauto.findwindows import find_window
import os
import coords
import pyautogui
import time

picture_path = ""


def init() -> None:
    global picture_path
    picture_path = os.path.join(os.getcwd(), "img")


def window_found(name: str) -> bool:
    try:
        find_window(title=name)
        return True
    except Exception:
        return False


def attempt_click(picture, region, game=False, click=True, conf=0.95) -> bool:
    global picture_path
    picture = os.path.join(picture_path, picture)

    try:
        if game:
            rect = coords.game()
        else:
            rect = coords.client()

        if region is not None:
            x = rect[0] + region[0]
            y = rect[1] + region[1]
            width = region[2] - region[0]
            height = region[3] - region[1]
            rect = (x, y, width, height)

        coordinates = pyautogui.locateCenterOnScreen(picture, confidence=conf)

        if coordinates is not None:
            if click:
                pyautogui.click(coordinates[0], coordinates[1])

            time.sleep(0.1)
            return True

    except Exception as e:
        print(e)
        return False


def close() -> None:
    time.sleep(5)
    exit(1)

