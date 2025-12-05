import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for index, voice in enumerate(voices):
    print(f"Index {index}: {voice.name} - {voice.id}")
    print(f"Gender: {voice.gender if hasattr(voice, 'gender') else 'N/A'}")
    print("---")