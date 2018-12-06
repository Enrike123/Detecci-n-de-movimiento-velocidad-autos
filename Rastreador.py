import cv2
import sys
from random import randint
import math

class Tracker():
  tracker_type = ""
  bboxes = []
  colors = []
  frame_width = 0.0
  camera_distance = 0.0
  focal_distance = 0.0
  field_view = 0.0
  frame_width_m = 0.0
  m_pixel = 0.0
  fact_km_h = 0.0
  frame_time = 0.0
  video_fps = 0.0
  frame_time = 0.0

  def init_parameters(self):
    # Calcula la distancia de la cámara
    # Distancia cámara al objeto en "metros"
    self.camera_distance = 13.153
    #Longitud Focal en "metros"
    self.focal_distance = 0.0039
    #Campo de visión de la cámara en Grados 
    self.field_view = 69
    #Distancia horizontal de la cámara en "metros"
    self.frame_width_m = round(2*(math.tan(math.radians(self.field_view*0.5))*self.camera_distance),3)
    #Conversión de un pixel a metros
    self.m_pixel = round(self.frame_width_m/self.frame_width,5)
    #Conversión de m/mseg a km/hr
    self.fact_km_h = 3600.0
    #Obtención de la cantidad de frame por segundo de la cámara
    self.frame_time = 1000/self.video_fps

  def create_tracker(self):
    #Se utiliza el tipo de Tracker "KFC" Kernelized Correlation Filters
    self.tracker_type = "KCF"
    #Crear Rastreador
    tracker = cv2.TrackerKCF_create()
    return tracker

  def open_video(self, path):
    #Abrir Video
    video = cv2.VideoCapture(path)
    #Salir del video si no se abrir
    if not video.isOpened():
      print("No se puede abrir el video")
      sys.exit()
    self.frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.video_fps = video.get(cv2.CAP_PROP_FPS)
    return video

  def simple_tracker(self, path):
    video = self.open_video(path)
    self.init_parameters()
    #Se lee el primer frame
    ok, frame = video.read()
    old_frame = frame
    if not ok:
      print('No se puede leer el archivo de video')
      sys.exit()
    #Se crea la velocidad instantanea en ese punto
    feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 7,blockSize = 7 )
    lk_params = dict(winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    #Se llama la función para crear el rastreador
    tracker = self.create_tracker()
    #Se define la caja delimitadora
    bbox = cv2.selectROI(frame, False)
    #Se inicializar el rastreador con el primer frame y la caja delimitadora
    ok = tracker.init(frame, bbox)
    velocity_list = []
    while True:
      #Se lee el nuevo frame
      ok, frame = video.read()
      if not ok:
        break
      
      #Se obtiene las velocidades instantaneas entre el antiguo frame y el nuevo frame
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
      good_new = p1[st==1]
      good_old = p0[st==1]
      for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        if a > bbox[0] and a < (bbox[0]+bbox[2]) and b > bbox[1] and b < (bbox[1]+bbox[3]):
          vel_ins = self.get_velocity_ins(a,b,c,d)
          velocity_list.append(vel_ins)
      #Se obtiene una velocidad promedio entre todos los puntos dentro de la caja delimitadora
      vel_ins_average = round(self.average_list(velocity_list),2)
      bbox_old = bbox
      #Se actualizar el rastreador
      ok, bbox = tracker.update(frame)
      other_vel_ins_average = round(self.get_velocity_ins(bbox_old[0],bbox_old[1],bbox[0],bbox[1]),2)
      
      if ok:
        #Se realiza el rastreo
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

      else :
        #Si falla el rastreo que muestre un mensaje de error
        cv2.putText(frame, "Error...", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
      #Se muestra la velocidad con el rastreo en la ventana del video
      cv2.putText(frame, "Velocidad Tracker" + str(other_vel_ins_average), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
      #Se muestra la velocidad con el TK (lukas kanade)
      cv2.putText(frame, "Velocidad TK: " + str(vel_ins_average), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
      #Se muestra el rastreador en la ventana
      cv2.imshow("Tracking", frame)
      #Si se desea salir del programa en ejecución se presiona ESC
      k = cv2.waitKey(1) & 0xff
      if k == 27 : break
      velocity_list = []

  def get_velocity_ins(self,x1,y1,x2,y2):
    #Disctancia euclidea entre puntos
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #Velocidad instantanea de objetos
    instant_velocity = distance/self.frame_time * self.m_pixel * self.fact_km_h
    return instant_velocity

  def average_list(self, el_list):
    #Se obtiene un promedio de las listas
    sum=0.0
    for i in range(0,len(el_list)):
        sum=sum+el_list[i]
    if len(el_list) > 0:
      return sum/len(el_list)
    else:
      return 0

if __name__ == '__main__' :
  mytra = Tracker()
  mytra.simple_tracker("videos/videotico.avi")
