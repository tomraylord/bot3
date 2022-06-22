import enum
import images
import regions
from util import window_found, attempt_click


class State(enum.Enum):
    start = 1
    client = 2
    home = 3
    champ_select = 10
    loading_into_game = 11
    in_game = 12
    post_game = 13


def change_state(next1: State) -> None:
    global current_state

    if next1 == current_state:
        return
    else:
        print(f"[State Update] From {current_state.name} ({current_state.value}) to {next1.name} ({next1.value}).")
        current_state = next1


def load_current_state() -> None:
    if window_found('League of Legends (TM) Client'):
        if attempt_click(images.recall, None, game=True, click=False) \
                or attempt_click(images.lock_cam, None, game=True, click=False) \
                or attempt_click(images.recall2, None, game=True, click=False):
            change_state(State.in_game)
        elif current_state is State.in_game:
            # Impossible
            return
        else:
            change_state(State.loading_into_game)
    elif window_found('League of Legends'):
        if attempt_click(images.champ_select, regions.choose_champ, click=False):
            change_state(State.champ_select)
        else:
            change_state(State.client)
    else:
        change_state(State.start)


current_state = State.start
