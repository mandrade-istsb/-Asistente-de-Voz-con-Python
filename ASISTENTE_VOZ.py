import wikipedia
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import datetime

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language='es-ES')
            rec = rec.lower()
    except sr.UnknownValueError:
        rec = "No te he entendido."
    except sr.RequestError:
        rec = "Lo siento, ha ocurrido un error al conectarse al servicio de reconocimiento de voz."
    return rec


def buscar_wikipedia():
    pregunta = listen()
    wikipedia.set_lang("es")
    try:
        res = wikipedia.summary(pregunta, sentences=1)
        talk(res)
        result_label.config(text=res)
    except wikipedia.exceptions.DisambiguationError:
        talk("Lo siento, hay varias opciones relacionadas con tu pregunta. Por favor, sé más específico.")
    except wikipedia.exceptions.PageError:
        talk("No he encontrado información relacionada con tu pregunta.")


def reproducir_video_youtube():
    talk("¿Qué video quieres reproducir en YouTube?")
    video = listen()
    url = f"https://www.youtube.com/results?search_query={video.replace(' ', '+')}"
    webbrowser.open(url)


def decir_hora_fecha_actual():
    now = datetime.datetime.now()
    hora = now.strftime("%H:%M")
    fecha = now.strftime("%d/%m/%Y")
    talk(f"La hora actual es {hora} y la fecha es {fecha}.")


app = tk.Tk()
app.title("IRIS")
app.geometry("400x400")  # Icono de la ventana

# Imagen de fondo de la ventana
imagen_fondo = Image.open("C:\\REPOSITORIO_CODIGOS\\PYTHON\\ECUADOR.jpg")
imagen_fondo = imagen_fondo.resize((400, 400))
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Creamos un canvas para poner la imagen de fondo
canvas = tk.Canvas(app, width=400, height=400)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

# imagen para el ícono del asistente
icon = Image.open("C:\\REPOSITORIO_CODIGOS\\PYTHON\\MANDRADE.jpg")
icon = icon.resize((100, 100))
icon = ImageTk.PhotoImage(icon)
app.iconphoto(True, icon)

talk("¡Hola! Soy Iris. ¿En qué puedo ayudarte?.")

# Botones para funciones de youtube, hora y fecha, wikipedia
search_button = tk.Button(app, text="Buscar en Wikipedia", command=buscar_wikipedia, bg="yellow", fg="white")
search_button.place(x=100, y=300)

youtube_button = tk.Button(app, text="Reproducir video de YouTube", command=reproducir_video_youtube, bg="red", fg="white")
youtube_button.place(x=100, y=330)

hora_fecha_button = tk.Button(app, text="Decir hora y fecha actual", command=decir_hora_fecha_actual, bg="green", fg="white")
hora_fecha_button.place(x=100, y=360)

result_label = tk.Label(app, text="", wraplength=380)
result_label.pack()

app.mainloop()