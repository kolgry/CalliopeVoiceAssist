# Calliope Voice Assistant

🌐 **Languages:** **English** | [Português (Brasil)](README.pt-BR.md)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
[![Demo on YouTube](https://img.shields.io/badge/Demo-YouTube-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=bBqjfVcH7jc)

A voice-controlled desktop assistant written in Python. Calliope listens for her name, understands spoken commands, and answers back with a synthesized voice. She can take notes, search Google, tell the time and date, read your daily agenda, recite poems, and even detect the emotion in your voice to pick music for you.

The project started as an experiment with Python voice-assistant libraries and grew into a small app with a graphical interface.

## Demo

[![Calliope Voice Assistant demo](https://img.youtube.com/vi/bBqjfVcH7jc/maxresdefault.jpg)](https://www.youtube.com/watch?v=bBqjfVcH7jc)

Watch the demo on YouTube: https://www.youtube.com/watch?v=bBqjfVcH7jc

## Features

- **Wake word:** say "Calliope" followed by a command.
- **Voice reminders:** dictate a note, which is saved to `anotacao.txt`, and have it read back to you.
- **Google search by voice:** say your query and Calliope opens the results in your browser.
- **Time and date:** ask what time it is or what day it is today.
- **Daily agenda:** reads today's upcoming events from an Excel spreadsheet (`agenda.xlsx`).
- **Poems:** recites a random poem from the Poetry Foundation dataset on Kaggle, filtered by length so it stays short enough to listen to.
- **Emotion analysis:** a TensorFlow/Keras model classifies the emotion in your voice (neutral, calm, happy, sad, angry, fear, disgust, surprised) and opens a matching YouTube track.
- **Graphical interface:** a PySide6 window with animated "listening" and "responding" indicators and live status text.
- **Cross-platform browser detection:** finds Chrome, Chromium, Firefox, Edge, Brave, Vivaldi, Opera or Safari on Windows, macOS and Linux, and falls back to the system default.

## Voice Commands

Start every command with the wake word, for example: *"Calliope, what time is it?"*

| Intent | Phrases |
| --- | --- |
| List capabilities | `what can you do`, `what do you do`, `functionalities`, `what do you know how to do`, `what else do you know how to do` |
| Take a note | `note`, `take note`, `remember`, `new note`, `new reminder`, `remind`, `reminder`, `write down`, `another note` |
| Search the web | `search`, `help`, `i need help`, `can you help me`, `i have a question`, `i have a doubt` |
| Current time | `what time is it`, `time`, `time now`, `what is the time` |
| Current date | `what day is today`, `what day is it`, `what day today` |
| Emotion mode | `emotion mode`, `activate emotion` |
| Today's agenda | `events today`, `schedule today`, `schedule`, `appointments today`, `today's events`, `events for today` |
| Read a poem | `read a poem`, `poem`, `recite a poem`, `tell me a poem`, `read me a poem`, `say a poem`, `poetry` |
| Exit | `quit` |

Commands are matched against these exact phrases. You can add your own in `modules/comandos_respostas.py`.

## How It Works

| Component | Technology |
| --- | --- |
| Speech recognition | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) with the Google Web Speech API (internet required) |
| Text to speech | [pyttsx3](https://pypi.org/project/pyttsx3/) (offline) |
| Emotion recognition | TensorFlow/Keras model (`models/speech_emotion_recognition.hdf5`) fed with MFCC features from [librosa](https://librosa.org/) |
| Poems | [kagglehub](https://pypi.org/project/kagglehub/) and pandas, using the Poetry Foundation dataset |
| Agenda | pandas reading `agenda.xlsx` |
| Interface | [PySide6](https://pypi.org/project/PySide6/) (Qt for Python) |
| Audio cues | playsound (`n1.mp3`, `n2.mp3`, `n3.mp3`) |

## Project Structure

```
CalliopeVoiceAssist/
├── assets/                  # GUI animations (listening / responding)
├── models/                  # Speech emotion recognition model
├── modules/
│   ├── browserManager.py    # Cross-platform browser detection and launching
│   ├── carrega_agenda.py    # Loads today's events from agenda.xlsx
│   ├── comandos_respostas.py# Command phrases and spoken responses
│   └── getPoem.py           # Fetches and filters random poems
├── recordings/              # Last captured microphone audio (speech.wav)
├── agenda.xlsx              # Your schedule
├── anotacao.txt             # Saved voice notes
├── assistente.py            # Console version of the assistant
├── assistente_thread.py     # Assistant worker thread used by the GUI
├── main_screen.py           # Main GUI window
├── run_gui.py               # Entry point for the GUI version
├── teste_instalacao.py      # Quick check that all libraries are installed
├── n1.mp3 / n2.mp3 / n3.mp3 # Sound effects
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A working microphone and speakers
- An internet connection (speech recognition and poem download)
- A system audio backend for PyAudio (on Linux, install PortAudio, e.g. `portaudio19-dev`, and `espeak` for pyttsx3)

### Installation

```bash
git clone https://github.com/kolgry/CalliopeVoiceAssist.git
cd CalliopeVoiceAssist

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install SpeechRecognition pyttsx3 playsound PyAudio \
            tensorflow numpy librosa matplotlib seaborn \
            pandas openpyxl kagglehub PySide6
```

Verify the installation:

```bash
python teste_instalacao.py
```

The script plays a sound, speaks a test phrase, and prints the version of each library.

### Configure Your Agenda

Create or edit `agenda.xlsx` with these columns:

| Column | Description |
| --- | --- |
| `data` | Event date |
| `hora` | Event time (`HH:MM:SS`) |
| `descricao` | What the event is |
| `responsavel` | Who is responsible |

Calliope reads out the events for today that start at or after the current hour.

### Run

Graphical interface:

```bash
python run_gui.py
```

Console only:

```bash
python assistente.py
```

When you hear the startup sound, say "Calliope" followed by a command. Say "Calliope, quit" to exit.

## Notes

- The first poem request downloads the dataset from Kaggle, so it may take a moment.
- The emotion analysis uses the last recording saved in `recordings/speech.wav`.
- Voice recognition quality depends on your microphone and background noise.

## Author

Created by [kolgry](https://github.com/kolgry) and [Junny](github.com/o0Junny0o).
