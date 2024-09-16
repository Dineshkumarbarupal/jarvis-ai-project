import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import music_library  # Assuming custom module music_library.py exists

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_google():
    webbrowser.open("https://google.com")
    speak("Opening Google")

def open_youtube():
    webbrowser.open("https://youtube.com")
    speak("Opening YouTube")

def play_music(song):
    if song in music_library.music:
        link = music_library.music[song]
        webbrowser.open(link)
        speak(f"Playing {song}")
    else:
        speak(f"Sorry, I could not find {song} in the music library")

def process_command(command):
    command = command.lower()
    if "open google" in command:
        open_google()
    elif "open youtube" in command:
        open_youtube()
    elif "play" in command:
        song = command.replace("play", "").strip()
        play_music(song)
    elif "shutdown" in command:
        speak("Shutting down...")
        return False
    return True

if __name__ == "__main__":
    speak("Initializing Jarvis....")

    # Adjust for ambient noise once
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    active = True
    while active:
        try:
            with sr.Microphone() as source:
                print("Listening for activation word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")

            if word.lower() == "jarvis":
                speak("Yes, I'm listening.")
                print("Jarvis activated")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")

                    active = process_command(command)

        except sr.UnknownValueError:
            speak("I did not understand, could you repeat that?")
        except sr.RequestError:
            speak("I'm having trouble connecting to the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
        
        # Pause to reduce CPU usage
        time.sleep(1)
