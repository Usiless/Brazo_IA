#include <Servo.h>                 // Se crean las funciones correspondientes
#include <ServoEasing.hpp>                 // Se crean las funciones correspondientes
ServoEasing serv1, serv2, serv3, serv4;  // Se declaran los servos // Se declaran los ejes para guardar los parametros de movimiento
int eje1 = 90;
int eje2 = 90;
int eje3 = 150;
int eje4 = 130;
int grados;
int x;
String servo;
String y;

void setup() {
  // Indicamos los pines para cada servo y sus posiciones iniciales
  serv1.attach(3, 90);
  //serv1.write(90);
  serv2.attach(5,90);
  // serv2.write(90);
  serv3.attach(6,150);
  // serv3.write(150);
  serv4.attach(9,130);
  // serv4.write(130);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  // Servo 1 -- Base
  // Se dan los parametros para el movimiento de Brazo en el respctivo pin analogico
  if (analogRead(0) < 200 && eje1 < 180) {
    eje1++;             // Aumentamos el eje
    serv1.write(eje1);  // Movemos el servo al valor dado por el eje
  } else if (analogRead(0) > 700 && eje1 > 0) {
    eje1--;
    serv1.write(eje1);
  }

  // Servo 2 -- Garra
  if (analogRead(1) < 200 && eje2 < 180) {
    eje2++;
    serv2.write(eje2);
  } else if (analogRead(1) > 700 && eje2 > 0) {
    eje2--;
    serv2.write(eje2);
  }

  // Servo 3 -- Movimiento Horizontal
  if (analogRead(2) < 200 && eje3 < 180) {
    eje3++;
    serv3.write(eje3);
  } else if (analogRead(2) > 700 && eje3 > 0) {
    eje3--;
    serv3.write(eje3);
  }
  // Servo 4 Movimiento Vertical
  if (analogRead(3) < 200 && eje4 < 180) {
    eje4++;
    serv4.write(eje4);
  } else if (analogRead(3) > 700 && eje4 > 0) {
    eje4--;
    serv4.write(eje4);
  }

  // //Pruebas COM
  //while (!Serial.available());
  y = Serial.readString();
  if (y == "0") {
    inicio();
    y = "";
  } else {
    servo = y[0];
    grados = y.substring(3).toInt();

    if (servo == "1") {
      serv1.easeTo(grados,40);
      Serial.print("izquierda, derecha ");
      Serial.print(y);
      y = "";
    }    
    if (servo == "2") {
      serv2.easeTo(grados,90);
      Serial.print("abre, cierra ");
      Serial.print(y);
      y = "";
    }
    if (servo == "3") {
      serv3.easeTo(grados,40);
      Serial.print("enfrente, atrás ");
      Serial.print(y);
      y = "";
    }
    if (servo == "4") {
      serv4.easeTo(grados,40);
      Serial.print("arriba, abajo ");
      Serial.print(y);
      y = "";
    }
    if (Serial.available()){
      Serial.flush();
      Serial.end();
      Serial.begin(9600);
    }
  }

  delay(10);  // Dejamos un pequeño espacio de tiempo para la ejecucion del programa
}

void inicio() {
  serv1.easeTo(90,40);
  serv2.easeTo(90,40);
  serv3.easeTo(150,40);
  serv4.easeTo(130,40);
  return;
}
