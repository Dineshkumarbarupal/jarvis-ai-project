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

def procescommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        split_command = c.lower().split(" ")
        if len(split_command) > 1:
            song = split_command[1]
            if song in music_library.music:
                link = music_library.music[song]
                webbrowser.open(link)
            else:
                print(f"Song '{song}' not found in music library")
        else:
            print("No song name provided to play")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    
    # Adjust for ambient noise just once
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening for activation word...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)  # Adjust timeout as needed
            word = r.recognize_google(audio)
            print(f"You said: {word}")

            if word.lower() == "jarvis":
                speak("Yes, I'm listening.")
                print("Jarvis activated")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"Command recognized: {command}")

                    procescommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")

        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")

        except Exception as e:
            print(f"Error: {e}")

        # Add a sleep delay to reduce CPU usage
        time.sleep(1)  # Reduce loop frequency to lower CPU load