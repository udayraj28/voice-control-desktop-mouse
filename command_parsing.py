import re

def parse_command(text):
    """
    Parses a voice command string and returns a dictionary
    with the detected intent and parameters.
    """

    text = text.lower().strip()

    # --- Regex Patterns ---

    move_pattern = re.compile(r'move (?:cursor|mouse)? (left|right|up|down)(?: by (\d+))?')
    arrow_key_pattern = re.compile(r'press arrow (left|right|up|down)')
    click_pattern = re.compile(r'(double click|right click|click)')
    scroll_pattern = re.compile(r'scroll (up|down)(?: (fast|slow|manually))?')
    continuous_scroll_pattern = re.compile(r'scroll (up|down) continuously')
    stop_scroll_pattern = re.compile(r'(stop scrolling|stop scroll)')
    type_pattern = re.compile(r'type (.+)')
    open_pattern = re.compile(r'open (.+)')
    desktop_pattern = re.compile(r'(go to desktop|show desktop)')

    # --- Matching Logic ---

    # Continuous scroll
    continuous_scroll_match = continuous_scroll_pattern.match(text)
    if continuous_scroll_match:
        direction = continuous_scroll_match.group(1)
        return {'intent': 'scroll_continuous', 'direction': direction}

    # Stop continuous scroll
    if stop_scroll_pattern.match(text):
        return {'intent': 'stop_scroll'}

    # Move mouse
    move_match = move_pattern.match(text)
    if move_match:
        direction = move_match.group(1)
        amount = move_match.group(2)
        amount = int(amount) if amount else 50
        return {'intent': 'move', 'direction': direction, 'amount': amount}

    # Arrow key press
    arrow_match = arrow_key_pattern.match(text)
    if arrow_match:
        key = arrow_match.group(1)
        return {'intent': 'keypress', 'key': f'arrow_{key}'}

    # Click
    click_match = click_pattern.match(text)
    if click_match:
        click_type = click_match.group(1)
        return {'intent': 'click', 'type': click_type}

    # Scroll
    scroll_match = scroll_pattern.match(text)
    if scroll_match:
        direction = scroll_match.group(1)
        speed = scroll_match.group(2) if scroll_match.group(2) else 'normal'
        return {'intent': 'scroll', 'direction': direction, 'speed': speed}

    # Type
    type_match = type_pattern.match(text)
    if type_match:
        content = type_match.group(1)
        return {'intent': 'type', 'content': content}

    # Open app
    open_match = open_pattern.match(text)
    if open_match:
        app_name = open_match.group(1)
        if "vs code" in app_name or "vscode" in app_name:
            return {'intent': 'open', 'app': 'vscode'}
        return {'intent': 'open', 'app': app_name}

    # Show desktop
    desktop_match = desktop_pattern.match(text)
    if desktop_match:
        return {'intent': 'show_desktop'}

    # Unknown
    return {'intent': 'unknown', 'raw_text': text}


# 🔍 Quick test
if __name__ == "__main__":
    test_commands = [
        "move cursor left by 100",
        "move mouse up",
        "click",
        "double click",
        "right click",
        "scroll down slowly",
        "scroll up fast",
        "scroll down manually",
        "scroll up continuously",
        "scroll down continuously",
        "stop scrolling",
        "stop scroll",
        "press arrow left",
        "type Hello, this is my AI assistant",
        "open notepad",
        "open vs code",
        "go to desktop",
        "random gibberish"
    ]

    for cmd in test_commands:
        result = parse_command(cmd)
        print(f"Command: {cmd}\nParsed: {result}\n")
