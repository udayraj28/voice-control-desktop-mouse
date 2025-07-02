# 🎤 Voice-Controlled Desktop Navigation System

A Python-based offline voice command system for full desktop navigation — move cursor, scroll, click, type, and launch apps using your voice. Built with [Vosk](https://alphacephei.com/vosk/), [PyAutoGUI](https://pyautogui.readthedocs.io/), and [sounddevice](https://python-sounddevice.readthedocs.io/).

---

## 🚀 Features

- 🗣️ **Wake word activation** – Say `"okay system"` to begin issuing commands.
- 🖱️ **Mouse control** – Move the cursor by direction and amount.
- 🖱️ **Click support** – Single, double, and right clicks.
- 🖱️ **Scroll control** – Scroll up/down fast or slow, including continuous scroll.
- ⌨️ **Arrow key emulation** – Say `"press arrow up"` etc.
- 📝 **Voice typing** – Dictate text into any application.
- 📂 **App launcher** – Open apps like Notepad, Calculator, or VS Code.
- 🖥️ **Show desktop** – Minimize all windows.
- 📴 **Deactivate mode** – Say `"stop listening"` to disable listening temporarily.

---

## 🗂️ File Structure

| File                 | Description                                                                                          |
|----------------------|------------------------------------------------------------------------------------------------------|
| `microphone.py`      | Listens for wake word and voice commands using Vosk; routes commands for parsing and execution.      |
| `command_parsing.py` | Converts natural voice input into structured command intents (via regex).                            |
| `voice_actions.py`   | Executes commands like mouse movement, scrolling, clicking, app launching, and typing.               |

---

## 🧰 Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- Microphone enabled and configured
- Download the Vosk model and extract it into a `model/` directory at the root

### 📦 Install Required Packages

```bash
pip install vosk pyautogui sounddevice 
