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

#Operaci�n:

Se debe utilizar: python tracking.py, estando en la misma direcci�n donde se descargue el programa.

Se selecciona el �rea donde se desea capturar el movimiento y luego presionar la tecla ENTER.

Para terminar el programa simplemente se presiona la tecla ESC.
-----------------------------------------------------------------

#OBSERVACIONES:

La c�mara esta ubicada aproximadamente a unos 10 metros de altura desde el suelo orientada para tomar una vista perpendicular al movimiento de los autos.

Sus caracter�sticas son:

Distancia focal=3.9
Distancia de C�mara al objeto: 13.153m aprox.
Campo de visi�n: 69�
Velocidad de captura: 25fps
Resoluci�n: 1920 * 1080 px

Se utiliza el algoritmo de seguimiento de Lukas Kanade y se utiliza el tipo de Rastreo "KFC" Kernelized Correlation Filters, que nos otorga la libreria de opencv. Ver como referencia el siguiente enlace:

Lukas Kanade: 

https://sandipanweb.wordpress.com/2018/02/25/implementing-lucas-kanade-optical-flow-algorithm-in-python/

KFC:

https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/.
-----------------------------------------------------------------

#EXPLICACION DEL PROGRAMA:

El programa primero abre el video deseado (los datos iniciales referentes a distancia y ubicaci�n son tomados en cuenta del video), luego se define la regi�n donde se desea captar el seguimiento. El programa capturara inicialmente el frame x y porteriormente crear� un bucle agreg�ndole el frame x+1, de estos dos obtendr� distancias entre puntos diferentes dentro de la regi�n seleccionada y mediante algunos c�lculos podremos obtener velocidades instantaneas entre todos estos puntos en el tiempo x y x+1. Por �ltimo obtendremos la velocidad promedio de todos estos puntos y ser� la que se mostrar� en el video en cada frame visualizado, esto se repetir� hasta la regi�n pierda al objeto.

