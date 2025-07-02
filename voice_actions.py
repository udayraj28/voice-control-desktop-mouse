import pyautogui
import subprocess
import platform
import threading
import time

# Flag to control continuous scrolling
scrolling = False
scroll_thread = None

def execute_command(parsed):
    global scrolling, scroll_thread
    intent = parsed.get('intent')

    if intent == 'move':
        direction = parsed.get('direction')
        amount = parsed.get('amount', 50)
        x, y = pyautogui.position()

        if direction == 'left':
            pyautogui.moveTo(x - amount, y)
        elif direction == 'right':
            pyautogui.moveTo(x + amount, y)
        elif direction == 'up':
            pyautogui.moveTo(x, y - amount)
        elif direction == 'down':
            pyautogui.moveTo(x, y + amount)

    elif intent == 'click':
        click_type = parsed.get('type')
        if click_type == 'click':
            pyautogui.click()
        elif click_type == 'double click':
            pyautogui.doubleClick()
        elif click_type == 'right click':
            pyautogui.rightClick()

    elif intent == 'scroll':
        direction = parsed.get('direction')
        speed = parsed.get('speed', 'normal')
        scroll_amount = 10 if speed == 'slowly' else 50
        repetitions = 20 if speed == 'slowly' else 50

        for _ in range(repetitions):
            if direction == 'down':
                pyautogui.scroll(-scroll_amount)
            elif direction == 'up':
                pyautogui.scroll(scroll_amount)
            time.sleep(0.05 if speed == 'slowly' else 0.01)

    elif intent == 'scroll_continuous':
        direction = parsed.get('direction')
        if scroll_thread is None or not scroll_thread.is_alive():
            scrolling = True
            scroll_thread = threading.Thread(target=continuous_scroll, args=(direction,))
            scroll_thread.start()

    elif intent == 'stop_scroll':
        scrolling = False

    elif intent == 'type':
        content = parsed.get('content', '')
        pyautogui.write(content)

    elif intent == 'open':
        app = parsed.get('app')
        open_app(app)

    elif intent == 'keypress':
        key = parsed.get('key')
        pyautogui.press(key.replace("arrow_", ""))  # e.g., 'arrow_left' → 'left'

    elif intent == 'show_desktop':
        minimize_all_windows()

    else:
        print("Unknown command intent")


def continuous_scroll(direction):
    global scrolling
    print(f"🌀 Starting continuous scroll {direction}")
    scroll_amount = 30
    while scrolling:
        if direction == 'down':
            pyautogui.scroll(-scroll_amount)
        elif direction == 'up':
            pyautogui.scroll(scroll_amount)
        time.sleep(0.05)
    print("🛑 Continuous scroll stopped.")


def open_app(app_name):
    system = platform.system()
    try:
        if system == 'Windows':
            if app_name == 'notepad':
                subprocess.Popen(['notepad.exe'])
            elif app_name == 'calculator':
                subprocess.Popen(['calc.exe'])
            elif app_name == 'vscode':
                subprocess.Popen(['code'])  # Assumes VS Code is in PATH
            else:
                print(f"App '{app_name}' not supported yet.")
        elif system == 'Linux':
            subprocess.Popen([app_name])
        elif system == 'Darwin':
            subprocess.Popen(['open', '-a', app_name])
        else:
            print(f"Unsupported OS: {system}")
    except Exception as e:
        print(f"❌ Failed to open app '{app_name}': {e}")


def minimize_all_windows():
    system = platform.system()
    try:
        if system == 'Windows':
            pyautogui.hotkey('win', 'd')
        elif system == 'Linux':
            pyautogui.hotkey('ctrl', 'alt', 'd')
        elif system == 'Darwin':
            pyautogui.hotkey('fn', 'f11')  # Often used for show desktop
    except Exception as e:
        print(f"❌ Failed to minimize windows: {e}")
