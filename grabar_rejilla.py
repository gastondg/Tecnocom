import cv2
import numpy as np
import time
from datetime import datetime

now = datetime.now()
now = now.strftime("%Y-%m-%d %H-%M")

"""  
A TENER EN CUENTA: 
- NO PONER PUNTOS
- NO COLOCAR BARRAS

Nombres válidos:
2019-10-20 18:45 contaminacion pelets
2019-11-05 08:30 contaminacion polvillo
"""

def get_elapsed_seconds(start):
  # devuelve el tiempo transcurrido, en segundos
  return int(time.time() - start)

def get_nuevo_vid(NOMBRE_VIDEO, frame_width, frame_height):
  """ Devuelve un nuevo cv2 writer de video """
  out = cv2.VideoWriter(NOMBRE_VIDEO, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
      15, (frame_width, frame_height))
  return out


from time import gmtime

print("Esperando a la hora indicada de produccion")
print()
print("No tocar la computadora")
print()
print("No apagar")


while ((gmtime().tm_hour - 3) != 5) and ((gmtime().tm_min) < 50) :
  time.sleep(1000)


path = "./Videos/"
NOMBRE_VIDEO = path + now + " rejilla" + "{}.avi"

cam_url = 'rtsp://10.10.4.151:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA=='

cap = cv2.VideoCapture(cam_url)

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("No se pudo abrir la camara, revise la url de la cámara")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print("Empezando a grabar video...")

i = 1

out = get_nuevo_vid(NOMBRE_VIDEO.format(i), frame_width, frame_height)

start = time.time()
total_elapsed = time.time()

while(get_elapsed_seconds(total_elapsed) < 22000):
  ret, frame = cap.read()

  if ret == True:

    # Escribir el frame en 'archivo.avi'
    out.write(frame)

    # Display the resulting frame
    frame = cv2.pyrDown(frame)
    frame = cv2.pyrDown(frame)
    cv2.imshow('Rejilla', frame)
    
    # 300 seg = 5 min
    if int(get_elapsed_seconds(start)) >= 300:
      # pasaron 5 min -> cambio el video 
      out.release()
      # incremento en 1 el marcador de video
      i += 1
      out = get_nuevo_vid(NOMBRE_VIDEO.format(i), frame_width, frame_height)
      start = time.time()

    k = cv2.waitKey(1)
    # Press Q on keyboard to stop recording
    if k == ord('q'):
      print("Bye")
      break
    
  # Break the loop
  else:
    break

  

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
