import cv2
import numpy as np
import time
import boto3
import logging


def get_elapsed_seconds(start):
  # devuelve el tiempo transcurrido, en segundos
  return int(time.time() - start)

def rescale_frame(frame, percent=75):
    scale_percent = percent / 100
    width = int(frame.shape[1] * scale_percent )
    height = int(frame.shape[0] * scale_percent )
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def get_silver_mask(corte):
  """ Devolvemos la silver mask """
  hsv = cv2.cvtColor(corte, cv2.COLOR_BGR2HSV)
  
  #mask = cv2.inRange(hsv, (0,0,130), (180,40,255))
  mask = cv2.inRange(hsv, (0,0,86), (255,90,255))
  
  return mask
  
def get_porcentaje_color(mask):
    """  
    unos = color , ceros = ausencia de color
    """ 
    unos = np.sum(mask == 255)
    #print("Numero de unos: " + str(unos))
    ceros = np.sum(mask == 0)
    #print("Numero de ceros: " + str(ceros))
    total = ceros + unos
    porcentaje_unos = (unos / total) * 100
    porcentaje_ceros = (ceros / total) * 100

    return porcentaje_unos, porcentaje_ceros

def enviar_sms(cliente,telefono="+543794409048", texto = "Alerta"):
  """
  ENVIA EL SMS
  """
  a = cliente.publish(PhoneNumber=telefono, Message=texto)
  return a

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='rejilla.log', filemode='a', format=FORMAT)

cam_url = 'rtsp://10.10.4.151:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA=='
cam_url = './Videos/Videos/2019-11-20 19-13 rejilla5.avi'

cap = cv2.VideoCapture(cam_url)

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("No se pudo abrir la camara, revise la url de la cámara")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

start = time.time()
total_elapsed = time.time()

# Creamos el objeto que manda SMS
client = boto3.client("sns", "us-east-1")

# Colocamos bandera de espera
wait_seconds = time.time()
wait = False

while(get_elapsed_seconds(total_elapsed) < 100):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    
    k = cv2.waitKey(1)

    # Resize for seeing
    frame = rescale_frame(frame, percent=25)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # defino la rejilla
    #x,y,w,h = 273, 150, 754, 331
    x, y, w, h = 115, 193, 618, 267
    rejilla = frame[y:y+h, x:x+w]
    
    # obtengo la mask con 1s y 0s
    mask = get_silver_mask(rejilla)
    # obtengo porcentaje de 0s y 1s
    porcentaje_unos, porcentaje_ceros = get_porcentaje_color(mask)
    """ print("Porcentaje ceros:")
    print(porcentaje_ceros)
    print("Porcentaje unos:")
    print(porcentaje_unos) """
      
    # if (porcentaje_unos > 50) and (not wait):
    if not wait and (int(porcentaje_ceros) > 47):
      print("Porcentaje ceros:")
      print(porcentaje_ceros)
      print("Porcentaje unos:")
      print(porcentaje_unos)
      print("Aca deberia haber una alerta con SNS")
      logging.warning("Rejilla comprometida")
      #print(enviar_sms(client, texto="alerta de llenado de rejilla"))
      wait_seconds = time.time()
      wait = True

    if wait and (get_elapsed_seconds(wait_seconds) > 60):
      # Si paso mas de 1 min cuando la bandera de espera era True, ya podemos mandar alertas nuevamente
      wait = False

    cv2.imshow('frame', frame)
    cv2.imshow('Mask', mask)

    # Presionar Q para salir
    if k == ord('q'):
      print("Bye")
      break

    # Break the loop
  else:
    break


# When everything done, release the video capture and video write objects
cap.release()
#out.release()

# Closes all the frames
cv2.destroyAllWindows()
