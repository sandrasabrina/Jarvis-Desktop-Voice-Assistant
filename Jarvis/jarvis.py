"""
Jarvis Voice Assistant
----------------------
Versão aprimorada com boas práticas de nomenclatura e legibilidade.
Objetivo: Tornar o código mais claro e de fácil manutenção.
"""

import datetime
import os
import random
import webbrowser
import pyautogui
import pyjokes
import pyttsx3
import speech_recognition as sr
import wikipedia

# ==========================
# Configurações do motor de voz
# ==========================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Define voz feminina
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

ASSISTANT_NAME_FILE = "assistant_name.txt"


# ==========================
# Funções utilitárias
# ==========================

def speak(text: str) -> None:
    """Converte texto em fala e o pronuncia."""
    engine.say(text)
    engine.runAndWait()


def get_current_time() -> None:
    """Informa a hora atual."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print(f"The current time is {current_time}")


def get_current_date() -> None:
    """Informa a data atual."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def load_assistant_name() -> str:
    """Carrega o nome do assistente, caso exista; caso contrário, retorna 'Jarvis'."""
    try:
        with open(ASSISTANT_NAME_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"


def set_assistant_name() -> None:
    """Permite ao usuário renomear o assistente."""
    speak("What would you like to name me?")
    new_name = take_voice_command()
    if new_name:
        with open(ASSISTANT_NAME_FILE, "w") as file:
            file.write(new_name)
        speak(f"Alright, I will be called {new_name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")


def greet_user() -> None:
    """Cumprimenta o usuário de acordo com o horário atual."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 16:
        greet = "Good afternoon!"
    elif 16 <= hour < 24:
        greet = "Good evening!"
    else:
        greet = "Good night, see you tomorrow."

    speak(greet)
    print(greet)

    assistant_name = load_assistant_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def take_screenshot() -> None:
    """Captura e salva uma captura de tela."""
    image = pyautogui.screenshot()
    image_path = os.path.expanduser("~/Pictures/screenshot.png")
    image.save(image_path)
    speak(f"Screenshot saved as {image_path}.")
    print(f"Screenshot saved as {image_path}.")


def play_music(song_name: str = None) -> None:
    """Reproduz uma música da pasta 'Músicas' do usuário."""
    music_directory = os.path.expanduser("~/Music")
    songs = os.listdir(music_directory)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(music_directory, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")


def take_voice_command() -> str | None:
    """Capta o áudio do microfone e converte em texto."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1

        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"Command: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
    except Exception as error:
        speak(f"An error occurred: {error}")
        print(f"Error: {error}")
    return None


def search_wikipedia(query: str) -> None:
    """Busca um resumo no Wikipedia com base na consulta."""
    try:
        speak("Searching Wikipedia...")
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
        print(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")


# ==========================
# Execução principal
# ==========================

def main():
    """Função principal que mantém o assistente em execução."""
    greet_user()

    while True:
        command = take_voice_command()
        if not command:
            continue

        if "time" in command:
            get_current_time()

        elif "date" in command:
            get_current_date()

        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in command:
            song = command.replace("play music", "").strip()
            play_music(song)

        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            webbrowser.open("https://google.com")

        elif "change your name" in command:
            set_assistant_name()

        elif "screenshot" in command:
            take_screenshot()
            speak("I've taken a screenshot, please check it.")

        elif "tell me a joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "shutdown" in command:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif "restart" in command:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif "offline" in command or "exit" in command:
            speak("Going offline. Have a good day!")
            break


if __name__ == "__main__":
    main()
