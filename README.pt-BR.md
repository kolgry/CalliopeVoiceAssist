# Calliope Voice Assistant

🌐 **Idiomas:** [English](README.md) | **Português (Brasil)**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white)
![PySide6](https://img.shields.io/badge/Interface-PySide6-41CD52?logo=qt&logoColor=white)
![Plataforma](https://img.shields.io/badge/Plataforma-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
[![Demo no YouTube](https://img.shields.io/badge/Demo-YouTube-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=bBqjfVcH7jc)
![Estrelas](https://img.shields.io/github/stars/kolgry/CalliopeVoiceAssist?style=flat)
![Forks](https://img.shields.io/github/forks/kolgry/CalliopeVoiceAssist?style=flat)
![Último commit](https://img.shields.io/github/last-commit/kolgry/CalliopeVoiceAssist)

Um assistente de voz para desktop escrito em Python. A Calliope espera ouvir o próprio nome, entende comandos falados e responde com voz sintetizada. Ela anota lembretes, pesquisa no Google, diz a hora e a data, lê sua agenda do dia, recita poemas e até detecta a emoção na sua voz para escolher uma música para você.

O projeto começou como um experimento com bibliotecas de assistentes de voz em Python e evoluiu para um pequeno aplicativo com interface gráfica.

## Demonstração

[![Demonstração do Calliope Voice Assistant](https://img.youtube.com/vi/bBqjfVcH7jc/maxresdefault.jpg)](https://www.youtube.com/watch?v=bBqjfVcH7jc)

Assista à demonstração no YouTube: https://www.youtube.com/watch?v=bBqjfVcH7jc

## Funcionalidades

- **Palavra de ativação:** diga "Calliope" seguido de um comando.
- **Lembretes por voz:** dite uma anotação, que é salva em `anotacao.txt`, e peça para ela ser lida de volta.
- **Pesquisa no Google por voz:** fale o que quer buscar e a Calliope abre os resultados no navegador.
- **Hora e data:** pergunte que horas são ou que dia é hoje.
- **Agenda do dia:** lê os próximos eventos de hoje a partir de uma planilha Excel (`agenda.xlsx`).
- **Poemas:** recita um poema aleatório do dataset Poetry Foundation (Kaggle), filtrado por tamanho para ficar curto o bastante para ouvir.
- **Análise de emoção:** um modelo TensorFlow/Keras classifica a emoção na sua voz (neutral, calm, happy, sad, angry, fear, disgust, surprised) e abre uma música correspondente no YouTube.
- **Interface gráfica:** janela em PySide6 com animações de "ouvindo" e "respondendo" e texto de status em tempo real.
- **Detecção de navegador multiplataforma:** encontra Chrome, Chromium, Firefox, Edge, Brave, Vivaldi, Opera ou Safari no Windows, macOS e Linux, com o navegador padrão do sistema como alternativa.

## Comandos de Voz

Comece todo comando com a palavra de ativação, por exemplo: *"Calliope, what time is it?"*

> Os comandos são reconhecidos **em inglês**, mesmo neste README em português.

| Intenção | Frases |
| --- | --- |
| Listar funções | `what can you do`, `what do you do`, `functionalities`, `what do you know how to do`, `what else do you know how to do` |
| Anotar um lembrete | `note`, `take note`, `remember`, `new note`, `new reminder`, `remind`, `reminder`, `write down`, `another note` |
| Pesquisar na web | `search`, `help`, `i need help`, `can you help me`, `i have a question`, `i have a doubt` |
| Hora atual | `what time is it`, `time`, `time now`, `what is the time` |
| Data atual | `what day is today`, `what day is it`, `what day today` |
| Modo emoção | `emotion mode`, `activate emotion` |
| Agenda de hoje | `events today`, `schedule today`, `schedule`, `appointments today`, `today's events`, `events for today` |
| Ler um poema | `read a poem`, `poem`, `recite a poem`, `tell me a poem`, `read me a poem`, `say a poem`, `poetry` |
| Sair | `quit` |

Os comandos são comparados com essas frases exatas. Você pode adicionar as suas em `modules/comandos_respostas.py`.

## Como Funciona

| Componente | Tecnologia |
| --- | --- |
| Reconhecimento de fala | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) com a API Google Web Speech (requer internet) |
| Síntese de voz | [pyttsx3](https://pypi.org/project/pyttsx3/) (offline) |
| Reconhecimento de emoção | Modelo TensorFlow/Keras (`models/speech_emotion_recognition.hdf5`) alimentado com features MFCC extraídas pelo [librosa](https://librosa.org/) |
| Poemas | [kagglehub](https://pypi.org/project/kagglehub/) e pandas, usando o dataset Poetry Foundation |
| Agenda | pandas lendo `agenda.xlsx` |
| Interface | [PySide6](https://pypi.org/project/PySide6/) (Qt para Python) |
| Sons de feedback | playsound (`n1.mp3`, `n2.mp3`, `n3.mp3`) |

## Estrutura do Projeto

```
CalliopeVoiceAssist/
├── assets/                  # Animações da interface (ouvindo / respondendo)
├── models/                  # Modelo de reconhecimento de emoção na fala
├── modules/
│   ├── browserManager.py    # Detecção e abertura de navegadores multiplataforma
│   ├── carrega_agenda.py    # Carrega os eventos de hoje do agenda.xlsx
│   ├── comandos_respostas.py# Frases de comando e respostas faladas
│   └── getPoem.py           # Busca e filtra poemas aleatórios
├── recordings/              # Último áudio capturado do microfone (speech.wav)
├── agenda.xlsx              # Sua agenda
├── anotacao.txt             # Anotações feitas por voz
├── assistente.py            # Versão do assistente para console
├── assistente_thread.py     # Thread do assistente usada pela interface
├── main_screen.py           # Janela principal da interface
├── run_gui.py               # Ponto de entrada da versão com interface
├── teste_instalacao.py      # Verifica se todas as bibliotecas estão instaladas
├── n1.mp3 / n2.mp3 / n3.mp3 # Efeitos sonoros
└── README.md
```

## Primeiros Passos

### Pré-requisitos

- Python 3.10 ou superior
- Microfone e alto-falantes funcionando
- Conexão com a internet (reconhecimento de fala e download dos poemas)
- Backend de áudio para o PyAudio (no Linux, instale o PortAudio, por exemplo `portaudio19-dev`, e o `espeak` para o pyttsx3)

### Instalação

```bash
git clone https://github.com/kolgry/CalliopeVoiceAssist.git
cd CalliopeVoiceAssist

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install SpeechRecognition pyttsx3 playsound PyAudio \
            tensorflow numpy librosa matplotlib seaborn \
            pandas openpyxl kagglehub PySide6
```

Verifique a instalação:

```bash
python teste_instalacao.py
```

O script toca um som, fala uma frase de teste e exibe a versão de cada biblioteca.

### Configure sua Agenda

Crie ou edite o `agenda.xlsx` com estas colunas:

| Coluna | Descrição |
| --- | --- |
| `data` | Data do evento |
| `hora` | Horário do evento (`HH:MM:SS`) |
| `descricao` | O que é o evento |
| `responsavel` | Quem é o responsável |

A Calliope lê os eventos de hoje que começam na hora atual ou depois dela.

### Executar

Interface gráfica:

```bash
python run_gui.py
```

Apenas console:

```bash
python assistente.py
```

Quando ouvir o som de inicialização, diga "Calliope" seguido de um comando. Diga "Calliope, quit" para encerrar.

## Observações

- O primeiro pedido de poema baixa o dataset do Kaggle, então pode levar alguns instantes.
- A análise de emoção usa a última gravação salva em `recordings/speech.wav`.
- A qualidade do reconhecimento de voz depende do seu microfone e do ruído ao redor.

## Autor

Criado por [kolgry](https://github.com/kolgry) and [Junny](https://github.com/o0Junny0o).
