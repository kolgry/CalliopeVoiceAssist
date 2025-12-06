import pyttsx3
import speech_recognition as sr
from playsound import playsound

import random
import datetime

from tensorflow.python.ops.metrics_impl import false_negatives



hour = datetime.datetime.now().strftime('%H:%M')
print(hour)
date = datetime.date.today().strftime('%d/%B/%Y')
print(date)
date = date.split('/')
print(date)
import webbrowser as wb
import tensorflow as tf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from modules.browserManager import BrowserManager
from modules import carrega_agenda, comandos_respostas, getPoem
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

meu_nome = 'Calliope'


browser_manager = BrowserManager()

def search(frase):
    url = 'https://www.google.com/search?q=' + frase
    browser_manager.open_url(url)

def speak(audio):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1)
    engine.say(audio)
    engine.runAndWait()

def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=0.8)
        print('Listening...')
        audio = microfone.listen(source)
        with open('recordings/speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    try:
        frase = microfone.recognize_google(audio)
        print('You said:' + frase)
    except sr.UnknownValueError:
        frase = ''
        print('Could not understand audio')
    return frase

#emoção
MODEL_TYPES = ['EMOÇÃO']

def load_model_by_name(model_type):
    if model_type == MODEL_TYPES[0]:
        model = tf.keras.models.load_model('models/speech_emotion_recognition.hdf5')
        model_dict = sorted(list(['neutral', 'calm', 'happy', 'sad', 'angry', 'fear', 'disgust', 'surprised']))
        SAMPLE_RATE = 48000
    return model, model_dict, SAMPLE_RATE

model_type = 'EMOÇÃO'
loaded_model = load_model_by_name(model_type)

model_type = 'EMOÇÃO'
loaded_model = load_model_by_name(model_type)

def predict_sound(AUDIO, SAMPLE_RATE, plot = True):
    results = []
    wav_data, sample_rate = librosa.load(AUDIO, sr=SAMPLE_RATE)

    clip, index = librosa.effects.trim(wav_data, top_db=60, frame_length=512, hop_length=64)
    splitted_audio_data = tf.signal.frame(clip, sample_rate, sample_rate, pad_end=True, pad_value=0)
    for i, data in enumerate(splitted_audio_data.numpy()):
        mfccs_features = librosa.feature.mfcc(y = data, sr = sample_rate, n_mfcc=40)

        mfccs_scaled_features = np.mean(mfccs_features.T, axis = 0)
        mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

        mfccs_scaled_features = mfccs_scaled_features[:,:,np.newaxis]

        predictions = loaded_model[0].predict(mfccs_scaled_features, batch_size=32)

        if plot:
            plt.figure(figsize=(len(splitted_audio_data), 5))
            plt.barh(loaded_model[1], predictions[0])
            plt.tight_layout()
            plt.show()

        predictions = predictions.argmax(axis = 1)

        predictions = predictions.astype(int).flatten()
        predictions = loaded_model[1][predictions[0]]
        results.append(predictions)

        result_str = 'PART ' + str(i) + ': ' + str(predictions).upper()

    count_results = [[results.count(x), x] for x in set(results)]

    return max(count_results)

def play_music_youtube(emocao):
    play = False
    if emocao == 'sad' or emocao == 'fear':
        url = 'https://www.youtube.com/watch?v=k32IPg4dbz0&ab_channel=Amelhorm%C3%BAsicainstrumental'
        play = browser_manager.open_url(url)
    elif emocao == 'angry' or emocao == 'surprised':
        url = 'https://www.youtube.com/watch?v=pWjmpSD-ph0&ab_channel=CassioToledo'
        play = browser_manager.open_url(url)
    return play

def test_models():
    audio_source = '/Users/profa/PycharmProjects/AssistenteVirtual/recordings/speech.wav'
    prediction = predict_sound(audio_source, loaded_model[2], plot = False)
    return prediction

#fimemocao

playing = False
mode_control = False
print('[INFO] Ready to Begin!')
playsound('n1.mp3')

while True:
    result = listen_microphone()

    if meu_nome in result:
        result = str(result.split(meu_nome + ' ')[1])
        result = result.lower()
        print('Caliope Ready!')

        command_type = None
        for i, cmd_list in enumerate(comandos):
            if result in cmd_list:
                command_type = i
                break

        match command_type:
            case 0:
                playsound('n2.mp3')
                speak('At this point my functions are: ' + respostas[0])

            case 1:
                playsound('n2.mp3')
                speak('Go ahead!')
                result = listen_microphone()
                anotacao = open('anotacao.txt', mode='a+', encoding='utf-8')
                anotacao.write(result + '\n')
                anotacao.close()
                speak(''.join(random.sample(respostas[1], k=1)))
                speak('Do you wish i read the reminders?')
                result = listen_microphone()
                if result == 'sim' or result == 'pode ler':
                    with open('anotacao.txt') as file_source:
                        lines = file_source.readlines()
                        for line in lines:
                            speak(line)
                else:
                    speak('Ok!')

            case 2:
                playsound('n2.mp3')
                speak(''.join(random.sample(respostas[2], k=1)))
                result = listen_microphone()
                search(result)

            case 3:
                playsound('n2.mp3')
                speak('It is ' + datetime.datetime.now().strftime('%H:%M'))

            case 4:
                playsound('n2.mp3')
                speak('Today is: ' + date[0] + ' of ' + date[1])

            case 5:
                mode_control = True
                playsound('n1.mp3')
                speak('Emotion Analisys Undergoing!')

            case 6:
                playsound('n2.mp3')
                if carrega_agenda.carrega_agenda():
                    speak("This are the events scheduled for today:")
                    for i in range(len(carrega_agenda.carrega_agenda()[1])):
                        speak(carrega_agenda.carrega_agenda()[1][i] + ' ' +
                              carrega_agenda.carrega_agenda()[0][i] + ' scheduled to ' +
                              str(carrega_agenda.carrega_agenda()[2][i]))
                else:
                    speak("There are no events scheduled for today starting from the current time!")

            case 7:
                playsound('n2.mp3')
                speak(''.join(random.sample(respostas[5], k=1)))

                title, author, content = getPoem.get_random_poem(truncate=True, filter_by_size=True)

                if content is None:
                    speak('Sorry, I could not load a poem at this moment.')
                else:
                    if title and author:
                        speak(f'The poem is titled: {title}, by {author}')
                    elif title:
                        speak(f'The poem is titled: {title}')
                    elif author:
                        speak(f'This poem is by {author}')

                    lines = str(content).split('\n')
                    for line in lines:
                        if line.strip():
                            speak(line)

                    speak('That was the poem!')

            case 8:  # Short poems - NEW CASE
                playsound('n2.mp3')
                speak('Here is a short poem for you!')

                title, author, content = getPoem.get_short_poem()

                if content is None:
                    speak('Sorry, I could not load a poem at this moment.')
                else:
                    if title and author:
                        speak(f'The poem is titled: {title}, by {author}')
                    elif title:
                        speak(f'The poem is titled: {title}')
                    elif author:
                        speak(f'This poem is by {author}')

                    lines = str(content).split('\n')
                    for line in lines:
                        if line.strip():
                            speak(line)

                    speak('That was the poem!')

            case 9:  # Medium poems - NEW CASE
                playsound('n2.mp3')
                speak('Here is a medium length poem for you!')

                title, author, content = getPoem.get_medium_poem()

                if content is None:
                    speak('Sorry, I could not load a poem at this moment.')
                else:
                    if title and author:
                        speak(f'The poem is titled: {title}, by {author}')
                    elif title:
                        speak(f'The poem is titled: {title}')
                    elif author:
                        speak(f'This poem is by {author}')

                    lines = str(content).split('\n')
                    for line in lines:
                        if line.strip():
                            speak(line)

                    speak('That was the poem!')

            case _:
                pass

        if mode_control:
            analyze = test_models()
            print(f'I noticed {analyze} in your voice!')
            if not playing:
                speak('Listen to Music!')
                playing = play_music_youtube(analyze[1])
                break

        if result == 'quit':
            speak(''.join(random.sample(respostas[4], k=1)))
            break
    else:
        playsound('n3.mp3')