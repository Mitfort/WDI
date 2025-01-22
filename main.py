import speech_recognition as sr
import pyttsx3
import webbrowser
import pyautogui
import time
import psutil
import wikipedia
import tkinter as tk
import threading
import sys

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

window = tk.Tk()
window.title("Voice Assistant")
window.geometry("400x600")
window.configure(bg="white")

label = tk.Label(window, text="🐱", font=("Arial", 200, "bold"))
label.pack(pady=20)

def speak(text):
    label.config(fg='black')
    engine.say(text)
    engine.runAndWait()

def listen():
    label.config(fg='green')
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nasłuchuję...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Rozpoznawanie...")
        query = recognizer.recognize_google(audio, language="pl-PL")
        print(f"Powiedziałeś: {query}")
    except Exception as e:
        print("Przepraszam, nie zrozumiałem. Czy możesz powtórzyć?")
        return None
    return query.lower()

def search_web(query):
    speak(f"Szukam {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

to_do_list = []

def add_to_do(task):
    to_do_list.append(task)
    speak(f"{task} dodano do listy zadań.")

def show_to_do_list():
    if not to_do_list:
        speak("Twoja lista zadań jest pusta.")
    else:
        speak("Oto twoja lista zadań:")
        for i, task in enumerate(to_do_list, 1):
            speak(f"{i}. {task}")
            
def open_application(app_name):
    speak(f"Otwieram {app_name}")
    
    pyautogui.press("win")
    time.sleep(1)
    
    pyautogui.write(app_name)
    time.sleep(1)
    
    pyautogui.press("enter")
    
def close_application(app_name):
    running_apps=psutil.process_iter(['pid','name'])
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in app_name.split() or app_name in sys_app:
            pid=app.info.get('pid')
            
            try:
                app_pid = psutil.Process(pid)
                app_pid.terminate()
                found=True
            except psutil.AccessDenied:
                print(f"Odmowa dostępu do zamknięcia procesu: {app_pid.info['name']}")
            except Exception as e:
                print(f"Nieoczekiwany błąd przy zamykaniu {app_pid.info['name']}: {e}")
            
        else: pass
    if not found:
        speak(f"nie znaleziono {app_name}")
    else:
        speak(f"zamknięto {app_name}" )

def voice_assistant():
    while True:    
        speak("Cześć, jak mogę Ci pomóc?")
        query = listen()

        if query is None:
            continue
        
        label.config(fg='green')
        
        if "lista zadań" in query:
            if "dodaj" in query:
                speak("Jakie zadanie chcesz dodać?")
                task = listen()
                add_to_do(task)
            elif "pokaż" in query:
                show_to_do_list()
    
        elif "powiedz mi" in query:
            question = query.replace('znajdź',"").strip()
            question = query.replace('powiedz mi',"").strip()
            answer = get_summary(question)
            speak(answer)
        elif "wyszukaj" in query:
            search = query.replace("wyszukaj","").strip()
            search_web(search)

        elif "wyjdź" in query or "do widzenia" in query:
            speak("Do widzenia!")
            window.destroy()
            sys.exit(0)
            break
            
        elif "otwórz" in query:
            app_name = query.replace("otwórz","").strip()
            open_application(app_name)
        
        elif "zamknij" in query:
            app_name = query.replace("zamknij","").strip()
            close_application(app_name)

        elif "utwórz" in query:
            speak("Jak chciałbyś nazwać swój nowy plik txt")
            filename = listen()
            speak(f"Powiedz jaki tekst powinienem zapisać do pliku {filename}.txt")
            content = listen()
            save_to_file(filename,content)
        else:
            speak("Przepraszam, nie rozumiem tego polecenia.")


def close_application(app_name):
    running_apps=psutil.process_iter(['pid','name'])
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in app_name.split() or app_name in sys_app:
            pid=app.info.get('pid')
            
            try:
                app_pid = psutil.Process(pid)
                app_pid.terminate()
                found=True
            except: pass
            
        else: pass
    if not found:
        speak(app_name+" nie znaleziona")
    else:
        speak(app_name+'('+sys_app+')'+' zamknieta')

def start_voice_assistant():
    threading.Thread(target=voice_assistant, daemon=True).start()

def get_summary(question):
    wikipedia.set_lang('pl')
    search_results = wikipedia.search(question)
    if search_results:
        page_title = search_results[0]
        try:
            summary = wikipedia.summary(page_title, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Zapytanie jest niejednoznaczne. Możliwe wyniki to: {e.options}"
        except wikipedia.exceptions.PageError:
            return "Nie znaleziono strony dla zapytania."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"
    else:
        return "Brak wyników wyszukiwania dla zapytania."
    
def save_to_file(filename,content):
    with open(filename,'a',encoding='utf-8') as file:
        file.write(content)
    speak("Pomyślnie zapisano dane do pliku")

if __name__ == "__main__":
    start_voice_assistant()
    window.mainloop()

