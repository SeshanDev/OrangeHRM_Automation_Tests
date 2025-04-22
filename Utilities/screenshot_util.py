import os
import time


def take_screenshot(driver, name):
    # Get the project root (one level up from the current file)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Create a path to the root-level Screenshots directory
    screenshots_dir = os.path.join(root_dir, "Screenshots")

    # Make sure the directory exists
    os.makedirs(screenshots_dir, exist_ok=True)

    # Create a timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Save the screenshot
    driver.save_screenshot(filepath)
    print(f"✅ Screenshot saved at: {filepath}")
