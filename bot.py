import time

import win32api
import win32con
import pyautogui
import images
import regions
import state
from util import close, attempt_click

champs = [images.tristana]


def start() -> None:
    debug_this_bot = False
    print("Starting bot.")

    print("Finding current state.")

    if debug_this_bot:
        print("[Debug] Debug mode: True")
        force_state = state.State.in_game

        debug(f"Forcing state to {force_state.name} ({force_state.value}).")
        state.change_state(force_state)
    else:
        state.load_current_state()

    time.sleep(1)

    if state.current_state is state.State.start:
        print("Please open the client first, then the bot.")
        close()
    elif state.current_state is state.State.champ_select:
        select_champ()
        play_game()
        post_game()
    elif state.current_state is state.State.in_game or state.current_state is state.State.loading_into_game:
        play_game()
        post_game()
    elif state.current_state is state.State.post_game:
        post_game()
    else:
        clear()

    while True:
        clear()
        search()

        if attempt_click(images.champ_select, regions.champ_select, click=False):
            select_champ()
            play_game()
            post_game()


def search() -> None:
    attempt_click(images.play_again, None, conf=0.8)
    attempt_click(images.play, regions.play_button, conf=0.5)
    attempt_click(images.party, regions.party_button)
    attempt_click(images.coop_vs_ai, regions.coop_vs_ai)
    attempt_click(images.inter_bots, regions.intermediate_bots, conf=0.8)
    attempt_click(images.confirm, regions.confirm)

    time.sleep(2)
    attempt_click(images.find_match, None)
    attempt_click(images.find_match_hover, None)

    while state.current_state is not state.State.champ_select:
        attempt_click(images.accept, regions.accept)
        time.sleep(1)
        state.load_current_state()


def select_champ() -> None:
    while state.current_state is state.State.champ_select:
        for champ in champs:
            if attempt_click(champ, regions.champ_select, click=False, conf=0.8):
                attempt_click(champ, regions.champ_select, conf=0.8)
                time.sleep(0.01)
                attempt_click(images.lock_in, regions.lockin)
                attempt_click(images.lock_in, regions.lockin)
                attempt_click(images.lock_in, regions.lockin)
        break

    while state.current_state is not state.State.in_game:
        state.load_current_state()
        time.sleep(1)


def play_game() -> None:
    last_check = 0
    stand_still = False
    while state.current_state is state.State.loading_into_game:
        time.sleep(1)
        state.load_current_state()
    while state.current_state is state.State.in_game:
        time.sleep(0.5)
        if attempt_click(images.lock_cam, None, click=False):
            attempt_click(images.lock_cam, None)

        if attempt_click(images.shop, None, click=False) and stand_still is False:
            stand_still = True
            time.sleep(75)
            debug("Having a nap rn")

        if attempt_click(images.level_up, None, click=False, conf=0.85):
            debug("Skill up")
            attempt_click(images.level_up, None, conf=0.85)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

        if attempt_click(images.shop, None, click=False):
            time.sleep(2)
        elif attempt_click(images.tower1, None, click=False, conf=0.35):
            debug("Halal Zone")
            pyautogui.moveTo(796, 621)
            move()
        elif attempt_click(images.tower2, None, click=False, conf=0.55):
            debug("Halal Zone 2")
            pyautogui.moveTo(796, 621)
            move()
        elif attempt_click(images.target1, None, click=False, conf=0.75):
            debug("Shooting ryze")
            attempt_click(images.target1, None, conf=0.75)
            attack_move(0.03)
        else:
            pyautogui.moveTo(1224, 250)
            attack_move()

        if last_check > 10:
            last_check = 0
            state.load_current_state()
        else:
            last_check = last_check + 1


def attack_move(time1=0.25) -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
    time.sleep(time1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)
    time.sleep(time1)


def move(time1=0.25) -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(time1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    time.sleep(time1)


def post_game() -> None:
    while not attempt_click(images.play_again, None, click=False):
        clear()

    attempt_click(images.cl_continue, None)
    attempt_click(images.play_again, None)
    time.sleep(2)
    attempt_click(images.find_match, regions.find_match)
    attempt_click(images.find_match_hover, regions.find_match)


def clear() -> None:
    if attempt_click(images.daily_play, None, click=False):
        finished = False
        while not finished:
            attempt_click(images.d_caitlyn, None)
            attempt_click(images.d_illaoi, None)
            attempt_click(images.d_ziggs, None)
            attempt_click(images.d_thresh, None)
            attempt_click(images.d_ekko, None)

            attempt_click(images.select, None)
            finished = attempt_click(images.ok3, None)

    attempt_click(images.skip_honour, None)
    attempt_click(images.cl_continue, None)
    attempt_click(images.ok, None)
    attempt_click(images.clash, None)
    attempt_click(images.ok2, None)


def debug(message) -> None:
    if debug:
        print("[Debug] %s @ %s" % (message, time.time()))
