DETECCION DE MOVIMIENTO Y CALCULO DE VELOCIDAD DE AUTOS:
-----------------------------------------------------------------
#DEPENDENCIAS:

cv2(opencv_contrib)
sys
math
PILL
-----------------------------------------------------------------
#REQUERIMIENTOS:

El programa esta desarrollado en Windows con python v3.6

#Operación:

Se debe utilizar: python tracking.py, estando en la misma dirección donde se descargue el programa.

Se selecciona el área donde se desea capturar el movimiento y luego presionar la tecla ENTER.

Para terminar el programa simplemente se presiona la tecla ESC.
-----------------------------------------------------------------

#OBSERVACIONES:

La cámara esta ubicada aproximadamente a unos 10 metros de altura desde el suelo orientada para tomar una vista perpendicular al movimiento de los autos.

Sus características son:

Distancia focal=3.9
Distancia de Cámara al objeto: 13.153m aprox.
Campo de visión: 69°
Velocidad de captura: 25fps
Resolución: 1920 * 1080 px

Se utiliza el algoritmo de seguimiento de Lukas Kanade y se utiliza el tipo de Rastreo "KFC" Kernelized Correlation Filters, que nos otorga la libreria de opencv. Ver como referencia el siguiente enlace:

Lukas Kanade: 

https://sandipanweb.wordpress.com/2018/02/25/implementing-lucas-kanade-optical-flow-algorithm-in-python/

KFC:

https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/.
-----------------------------------------------------------------

#EXPLICACION DEL PROGRAMA:

El programa primero abre el video deseado (los datos iniciales referentes a distancia y ubicación son tomados en cuenta del video), luego se define la región donde se desea captar el seguimiento. El programa capturara inicialmente el frame x y porteriormente creará un bucle agregándole el frame x+1, de estos dos obtendrá distancias entre puntos diferentes dentro de la región seleccionada y mediante algunos cálculos podremos obtener velocidades instantaneas entre todos estos puntos en el tiempo x y x+1. Por último obtendremos la velocidad promedio de todos estos puntos y será la que se mostrará en el video en cada frame visualizado, esto se repetirá hasta la región pierda al objeto.

