from PySide6.QtCore import QThread, Signal
import pyttsx3
import speech_recognition as sr
from playsound import playsound

import random
import datetime
import sys
import webbrowser as wb
import tensorflow as tf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from modules import carrega_agenda, comandos_respostas, getPoem
from modules.browserManager import BrowserManager
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

class AssistenteWorker(QThread):
    status_updated = Signal(str)

    browser_manager = BrowserManager()
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.meu_nome = 'Calliope'
        self.browser_manager = BrowserManager()
        
        self.hour = datetime.datetime.now().strftime('%H:%M')
        self.date = datetime.date.today().strftime('%d/%B/%Y')
        self.date = self.date.split('/')
        
        self.model_type = 'EMOÇÃO'
        self.loaded_model = self.load_model_by_name(self.model_type)
        
        self.playing = False
        self.mode_control = False
        
        self.status_updated.connect(self.main_window.status_signal.status_changed.emit)

    def load_model_by_name(self, model_type):
        if model_type == 'EMOÇÃO':
            model = tf.keras.models.load_model('models/speech_emotion_recognition.hdf5')
            model_dict = sorted(list(['neutral', 'calm', 'happy', 'sad', 'angry', 'fear', 'disgust', 'surprised']))
            SAMPLE_RATE = 48000
        return model, model_dict, SAMPLE_RATE

    def speak(self, audio, keep_status=None):
        try:
            if keep_status is None:
                self.status_updated.emit("responding")
            
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 120)
            engine.setProperty('volume', 1)
            engine.say(str(audio))
            engine.runAndWait()
            
            if keep_status is not None:
                self.status_updated.emit(keep_status)
            else:
                self.status_updated.emit("listening")
        except Exception as e:
            print(f'Erro ao falar: {e}')
            if keep_status is not None:
                self.status_updated.emit(keep_status)
            else:
                self.status_updated.emit("listening")

    def listen_microphone(self):
        self.status_updated.emit("listening")
        microfone = sr.Recognizer()
        with sr.Microphone() as source:
            microfone.adjust_for_ambient_noise(source, duration=0.8)
            audio = microfone.listen(source)
            with open('recordings/speech.wav', 'wb') as f:
                f.write(audio.get_wav_data())

        try:
            frase = microfone.recognize_google(audio)
            print('You said:' + frase)
        except sr.UnknownValueError:
            frase = ''
            self.status_updated.emit("dont understand")
            print('Could not understand audio')
        return frase

    def search(self, frase):
        self.status_updated.emit("search | searching...")
        url = 'https://www.google.com/search?q=' + frase
        self.browser_manager.open_url(url)

    def predict_sound(self, AUDIO, SAMPLE_RATE, plot=True):
        results = []
        wav_data, sample_rate = librosa.load(AUDIO, sr=SAMPLE_RATE)

        clip, index = librosa.effects.trim(wav_data, top_db=60, frame_length=512, hop_length=64)
        splitted_audio_data = tf.signal.frame(clip, sample_rate, sample_rate, pad_end=True, pad_value=0)
        for i, data in enumerate(splitted_audio_data.numpy()):
            mfccs_features = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=40)

            mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
            mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

            mfccs_scaled_features = mfccs_scaled_features[:, :, np.newaxis]

            predictions = self.loaded_model[0].predict(mfccs_scaled_features, batch_size=32)

            if plot:
                plt.figure(figsize=(len(splitted_audio_data), 5))
                plt.barh(self.loaded_model[1], predictions[0])
                plt.tight_layout()
                plt.show()

            predictions = predictions.argmax(axis=1)

            predictions = predictions.astype(int).flatten()
            predictions = self.loaded_model[1][predictions[0]]
            results.append(predictions)

            result_str = 'PART ' + str(i) + ': ' + str(predictions).upper()

        count_results = [[results.count(x), x] for x in set(results)]

        return max(count_results)

    def play_music_youtube(self, emocao):
        play = False
        if emocao == 'sad' or emocao == 'fear':
            wb.get(self.chrome_path).open('https://www.youtube.com/watch?v=k32IPg4dbz0&ab_channel=Amelhorm%C3%BAsicainstrumental')
            play = True
        if emocao == 'angry' or emocao == 'surprised':
            wb.get(self.chrome_path).open('https://www.youtube.com/watch?v=pWjmpSD-ph0&ab_channel=CassioToledo')
            play = True
        return play

    def test_models(self):
        audio_source = 'recordings/speech.wav'
        prediction = self.predict_sound(audio_source, self.loaded_model[2], plot=False)
        return prediction

    def run(self):
        print('[INFO] Ready to Begin!')
        playsound('n1.mp3')

        while True:
            try:
                result = self.listen_microphone()

                if self.meu_nome in result:
                    result = str(result.split(self.meu_nome + ' ')[1])
                    result = result.lower()
                    print('Calliope Ready!')
                    
                    if result in comandos[0]:
                        playsound('n2.mp3')
                        self.speak('At this point my functions are: ' + respostas[0])

                    if result in comandos[1]:
                        playsound('n2.mp3')
                        self.speak('Go ahead!')
                        result = self.listen_microphone()
                        anotacao = open('anotacao.txt', mode='a+', encoding='utf-8')
                        anotacao.write(result + '\n')
                        anotacao.close()
                        self.speak(''.join(random.sample(respostas[1], k=1)))
                        self.speak('Do you wish i read the reminders?')
                        result = self.listen_microphone()
                        if result == 'sim' or result == 'pode ler':
                            with open('anotacao.txt') as file_source:
                                lines = file_source.readlines()
                                for line in lines:
                                    self.speak(line)
                        else:
                            self.speak('Ok!')

                    if result in comandos[2]:
                        playsound('n2.mp3')
                        self.speak(''.join(random.sample(respostas[2], k=1)))
                        self.status_updated.emit('search')
                        result = self.listen_microphone()
                        self.search(result)

                    if result in comandos[3]:
                        playsound('n2.mp3')
                        self.speak('It is ' + datetime.datetime.now().strftime('%H:%M'))

                    if result in comandos[4]:
                        playsound('n2.mp3')
                        self.speak('Today is: ' + self.date[0] + ' of ' + self.date[1])

                    if result in comandos[5]:
                        self.mode_control = True
                        playsound('n1.mp3')
                        self.speak('Emotion Analisys Undergoing!')

                    if self.mode_control:
                        analyze = self.test_models()
                        print(f'I noticed {analyze} in your voice!')
                        if not self.playing:
                            self.speak('Listen to Music!')
                            self.playing = self.play_music_youtube(analyze[1])
                            break

                    if result in comandos[6]:
                        playsound('n2.mp3')
                        if carrega_agenda.carrega_agenda():
                            self.speak("This are the events scheduled for today:")
                            for i in range(len(carrega_agenda.carrega_agenda()[1])):
                                self.speak(carrega_agenda.carrega_agenda()[1][i] + ' ' + carrega_agenda.carrega_agenda()[0][i] + ' scheduled to ' + str(carrega_agenda.carrega_agenda()[2][i]))
                            else:
                                self.speak('"There are no events scheduled for today starting from the current time!')

                    if result in comandos[7]:
                        playsound('n2.mp3')
                        self.speak(''.join(random.sample(respostas[5], k=1)))

                        print('[INFO] Carregando poema...')
                        title, author, content = getPoem.get_random_poem()

                        if content is None:
                            self.speak('Sorry, I could not load a poem at this moment.')
                            self.status_updated.emit('Error loading poem')
                            print('[ERROR] Falha ao carregar poema')
                        else:
                            print(f'[INFO] Poema carregado: {title} por {author}')
                            
                            status_text = ''
                            if title and author:
                                status_text = f'{title} | by {author}'
                            elif title:
                                status_text = f'{title}'
                            elif author:
                                status_text = f'by {author}'
                            
                            self.status_updated.emit(status_text)
                            
                            if title and author:
                                self.speak(f'The poem is titled: {title}, by {author}', keep_status=status_text)
                            elif title:
                                self.speak(f'The poem is titled: {title}', keep_status=status_text)
                            elif author:
                                self.speak(f'This poem is by {author}', keep_status=status_text)
                            
                            lines = str(content).split('\n')
                            print(f'[INFO] Total de linhas: {len(lines)}')
                            for i, line in enumerate(lines):
                                clean_line = line.strip()
                                if clean_line:
                                    print(f'[INFO] Lendo linha {i + 1}: {clean_line[:50]}...')
                                    self.speak(clean_line, keep_status=status_text)

                            self.speak('That was the poem!')
                            self.status_updated.emit('listening')

                    if result == 'quit':
                        self.speak(''.join(random.sample(respostas[4], k=1)))
                        break
                else:
                    playsound('n3.mp3')
                    
            except Exception as e:
                print(f'[ERROR] {str(e)}')
