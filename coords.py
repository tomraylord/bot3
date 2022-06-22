import win32gui


def game():
    hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client')
    rect = win32gui.GetWindowRect(hwnd)
    return rect


def client():
    hwnd = win32gui.FindWindow(None, 'League of Legends')
    rect = win32gui.GetWindowRect(hwnd)
    return rect
