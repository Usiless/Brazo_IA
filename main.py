#pip install SpeechRecognition, pip install pyaudio, pip install pocketsphinx, python -m speech_recognition download es-ES
import keyboard
import speech_recognition as sr

from serial import Serial
import time
from IA import DocTypeRec

arduino = Serial(port='COM4', baudrate=9600, timeout=0.1)

def write_read(x): #Comunicación con el arduino
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def transcribe_speech(): #Reconocimiento de voz
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Habla algo...")
        # recognizer.adjust_for_ambient_noise(source)  # Ajusta el ruido ambiental
        try:
            audio = recognizer.listen(source,10,3)
        except sr.exceptions.WaitTimeoutError  as e:
            print(f"Error en la solicitud. Tiempo de espera agotado")
            time.sleep(10)
            return None
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print("Texto reconocido: ", text)
        return text
    except sr.UnknownValueError:
        print("No se pudo entender el habla.")
        return None
    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return None

if __name__ == "__main__":
    while True:
        print ("Presiona 'Espacio' para hablar. Presiona 'Escape' para salir.")
        if keyboard.is_pressed("space"): #Activar micro
            text = transcribe_speech()
            if text != None:
                try:
                    servo, grados = DocTypeRec(text)
                    if isinstance(servo, int):
                        print(servo, grados)
                        value = write_read(f"{servo}, {grados}")
                        print(value)
                    else:
                        cant_elem = len(servo)
                        aux = []
                        for i in range(0,cant_elem):
                            value = write_read(f"{servo[i]}, {grados[i]}")
                            print(value)
                            print(f"{servo[i]}, {grados[i]}")
                            time.sleep(0.5)
                except TypeError as e:
                    print(f"Comando no especificado: {e}")
                time.sleep(2.5)
        if keyboard.is_pressed("5"): #Saludar
            text = "hola"
            servo, grados = DocTypeRec(text)
            cant_elem = len(servo)
            for i in range(0,cant_elem):
                value = write_read(f"{servo[i]}, {grados[i]}")
                print(value)
                print(f"{servo[i]}, {grados[i]}")
                time.sleep(0.5)
        if keyboard.is_pressed("up"):
            text = "movete hacia arriba"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("down"):
            text = "movete hacia abajo"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("left"):
            text = "movete hacia izquierda"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("right"):
            text = "movete hacia derecha"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("1"):
            text = "movete el frente"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("3"):
            text = "movete hacia atrás"
            if text != None:
                servo, grados = DocTypeRec(text)
                print(servo, grados)
                value = write_read(f"{servo}, {grados}")
                print(value)
                time.sleep(2.5)
        if keyboard.is_pressed("0"): #Reiniciar posición
            print(0)
            value = write_read("0")
        if keyboard.is_pressed("esc"):
            break