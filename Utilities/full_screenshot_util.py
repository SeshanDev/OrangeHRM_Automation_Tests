import os
import time
import pyautogui

def take_fullscreen_screenshot(name):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    screenshots_dir = os.path.join(root_dir, "Screenshots")

    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{name}_FULL_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"🖥️ Fullscreen screenshot saved: {filepath}")
