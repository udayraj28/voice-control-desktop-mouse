import queue
import sounddevice as sd
import vosk
import sys
import json

from command_parsing import parse_command
from voice_actions import execute_command

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

WAKE_WORD = "okay system"

def listen_offline_with_wake():
    model = vosk.Model(r"D:\voice_control_project\model\vosk-model-small-en-us-0.15")
    recognizer = vosk.KaldiRecognizer(model, 16000)
    active = False

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🟢 Listening offline... Say 'okay system' to activate.")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print(f"🎙️ Recognized: {text}")

                    if not active:
                        # Wake word detection
                        if WAKE_WORD in text.lower():
                            print("✅ Wake word detected! Listening for commands...")
                            active = True
                    else:
                        # Check for deactivation
                        if text.lower() in ["stop listening", "go to sleep", "deactivate"]:
                            print("🛑 Deactivating. Say 'okay system' again to reactivate.")
                            active = False
                        else:
                            parsed_command = parse_command(text)
                            print(f"🧠 Parsed command: {parsed_command}")
                            execute_command(parsed_command)

if __name__ == "__main__":
    listen_offline_with_wake()
