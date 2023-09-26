Aquí está el readme.md actualizado con la información sobre el archivo arduino.ino. Espero que te sea útil.

# Proyecto de control de servomotores con Arduino y reconocimiento de voz

Este proyecto consiste en un programa en Python que permite controlar uno o más servomotores conectados a un Arduino mediante comandos de voz y análisis de texto.

## Instalación

Para instalar las librerías necesarias se puede usar el comando pip:

```
pip install keyboard
pip install speech_recognition
pip install pyserial
pip install spacy
python -m spacy download es_dep_news_trf
```

Para cargar el código en el Arduino se debe abrir el IDE y seleccionar el puerto COM correspondiente. El código se encuentra en el archivo arduino.ino.

## Uso

Para usar el programa se debe ejecutar el archivo main.py desde la terminal o desde un editor de código. El programa mostrará un mensaje indicando que se presione la tecla 'Espacio' para hablar o la tecla 'Escape' para salir. Al presionar 'Espacio' se activará el micrófono y se podrá decir un comando de voz. El programa reconocerá el texto y lo procesará con el archivo IA.py, que devolverá los parámetros del servomotor correspondiente al comando. Estos parámetros son el número de servo (1, 2 o 3) y los grados a los que debe girar (0 a 180 o -1 para girar continuamente). El programa enviará estos parámetros al Arduino mediante el puerto serie y el Arduino moverá el servo según lo indicado.

El programa también permite controlar los servos mediante las teclas del teclado. Las teclas disponibles son:

- 5: Saludar moviendo los tres servos
- Arriba: Mover el servo 4 hacia arriba
- Abajo: Mover el servo 4 hacia abajo
- Izquierda: Mover el servo 1 hacia la izquierda
- Derecha: Mover el servo 1 hacia la derecha
- 1: Mover el servo 3 hacia el frente
- 3: Mover el servo 3 hacia atrás
- 0: Reiniciar la posición de los servos

Los comandos de voz disponibles son:

- Hola: Saludar moviendo los servos, 3 y 2. El servo 2 abre y cierra la garra
- Movete hacia arriba: Mover el servo 4 hacia arriba
- Movete hacia abajo: Mover el servo 4 hacia abajo
- Movete hacia izquierda: Mover el servo 1 hacia la izquierda
- Movete hacia derecha: Mover el servo 1 hacia la derecha
- Movete al frente: Mover el servo 3 hacia el frente
- Movete hacia atrás: Mover el servo 3 hacia atrás

## Explicación del código

El código se divide en dos archivos principales: main.py y IA.py.

### main.py

Este archivo contiene las funciones principales del programa:

- write_read(x): Esta función recibe una cadena x con los parámetros del servo y la envía al Arduino por el puerto serie. Luego espera una respuesta del Arduino y la devuelve como una cadena.
- transcribe_speech(): Esta función activa el micrófono y graba el audio durante 10 segundos o hasta que se detecte un silencio de 3 segundos. Luego usa la librería speech_recognition para reconocer el texto del audio usando el servicio de Google. Si hay algún error o no se reconoce nada, devuelve None. Si se reconoce algo, lo imprime y lo devuelve como una cadena.
- main(): Esta función contiene el bucle principal del programa. Primero crea un objeto de la clase Servo, que está definida en IA.py, e inicializa la comunicación con el Arduino. Luego entra en un bucle infinito que espera a que se presione alguna tecla. Si se presiona 'Espacio', llama a la función transcribe_speech() y le pasa el texto reconocido al objeto Servo, que devuelve los parámetros del servo correspondiente al comando. Si se presiona alguna otra tecla, genera un texto equivalente al comando y lo pasa al objeto Servo. Finalmente, llama a la función write_read() con los parámetros del servo y espera una respuesta del Arduino.

### IA.py

Este archivo contiene la clase Servo, que se encarga de procesar el texto y generar los parámetros del servo.

- \_\_init\_\_(): Este método inicializa los atributos de la clase, que son los ángulos de los tres servos y un diccionario que asocia cada comando con una función.
- DocTypeRec(text): Este método recibe una cadena de texto y la compara con las claves del diccionario. Si encuentra una coincidencia, llama a la función correspondiente y devuelve los parámetros del servo. Si no encuentra ninguna coincidencia, devuelve None.
- hola(): Esta función devuelve una lista de tuplas con los parámetros de los tres servos para saludar
- defined_mov(doc): Esta función recibe un objeto doc de spacy y usa el matcher para reconocer el comando de movimiento. Luego recorre el doc y busca el adverbio o el pronombre que indica la dirección. Finalmente, devuelve el número de servo y los grados correspondientes a esa dirección según el diccionario directions.

### arduino.ino

Este archivo contiene el código que se carga en el Arduino para controlar los servos.

- Se incluyen las librerías Servo.h y ServoEasing.hpp para manejar los servos y sus movimientos suavizados.
- Se crean cuatro objetos de la clase ServoEasing para cada uno de los servos conectados a los pines 3, 5, 6 y 9.
- Se declaran cuatro variables enteras para guardar los ángulos de cada servo, inicializados en 90, 90, 150 y 130 respectivamente.
- Se declaran tres variables para guardar los datos recibidos por el puerto serie: una cadena para el número de servo, otra cadena para los grados y un entero para convertir la segunda cadena.
- En el setup() se inicializan los servos con el método attach() indicando el pin y el ángulo inicial. También se inicia la comunicación serie con el método Serial.begin() indicando la velocidad de 115200 baudios. Se establece el tiempo máximo de espera para leer datos con Serial.setTimeout() a 1 milisegundo.
- En el loop() se lee el valor analógico de cuatro potenciómetros conectados a los pines A0, A1, A2 y A3. Estos valores se usan para controlar manualmente los servos con las siguientes condiciones:
    - Si el valor es menor que 200 y el ángulo del servo es menor que 180, se incrementa el ángulo en una unidad y se escribe en el servo con el método write().
    - Si el valor es mayor que 700 y el ángulo del servo es mayor que 0, se decrementa el ángulo en una unidad y se escribe en el servo con el método write().
    - Cada potenciómetro controla un servo distinto: A0 controla el servo 1 (base), A1 controla el servo 2 (garra), A2 controla el servo 3 (movimiento horizontal) y A3 controla el servo 4 (movimiento vertical).
- También se lee la cadena enviada por el puerto serie con Serial.readString(). Si la cadena es "0", se llama a la función inicio() que reinicia la posición de los servos. Si no, se extrae el primer carácter de la cadena y se guarda en la variable servo. Luego se extrae el resto de la cadena a partir del tercer carácter y se convierte a entero con toInt(), guardándolo en la variable grados. Estas variables indican el número de servo y los grados a los que debe moverse según el comando de voz procesado por IA.py.
- Se usa un bloque if para comparar la variable servo con cada uno de los posibles valores ("1", "2", "3" o "4"). Si hay una coincidencia, se llama al método easeTo() del objeto ServoEasing correspondiente, pasándole como argumentos la variable grados y una duración fija (40 o 90 milisegundos según el caso). Este método hace que el servo se mueva suavemente al ángulo indicado en la duración especificada. También se imprime por el puerto serie un mensaje indicando qué movimiento se ha realizado y qué datos se han recibido.
- Al final del loop() se introduce un pequeño retraso de 10 milisegundos para facilitar el movimiento de los servos
