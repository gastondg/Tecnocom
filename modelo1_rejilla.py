import cv2
import numpy as np
import time
import boto3
import logging
from datetime import datetime



def unos_blur(blur, mogSub):
  """
  Devuelve la diferencia de pixeles que hay entre el fondo anterior y este
  Es decir la cantidad de unos que detecta
  """
  x, y, w, h = 90, 74, 678, 223
  corte = blur[y:y+h, x:x+w]
  # Remuevo el fondo
  mask_mog = mogSub.apply(corte)
  # devuelvo unos que encuentra
  return np.count_nonzero(mask_mog)

def get_espacio_movimiento(frame):
  x, y, w, h = 90, 74, 678, 223
  corte_movimiento = frame[y:y+h, x:x+w]
  return corte_movimiento

def get_espacio_llenado(frame):
  x, y, w, h = 115, 193, 618, 267
  rejilla = frame[y:y+h, x:x+w]
  return rejilla

def inicio_lista():
  i=2
  lista=[]
  return i, lista

def get_hour():
  return time.gmtime().tm_hour

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
  
  if get_hour() < 18:
    mask = cv2.inRange(hsv, (30,0,92), (202,117,255))
  else: 
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

def get_fecha():
  fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return fecha

def is_producing(lista):
    
    list = np.array(lista)
    minimo = list.min()
    print()
    print("Minimo de la lista: " + str(minimo))
    if minimo > 20:
        return True
    return False

def en_produccion(movimiento, mogSub, i, lista_unos_fondo, produccion, prod_frame_anterior, porcentaje):
  """
  Devuelve True si esta en produccion o False si no
  """
  # Agrego unos a la lista
  unos_movimiento = unos_blur(movimiento, mogSub)
  lista_unos_fondo.append(unos_movimiento)

  if i % 75 == 0:
    prod_frame_anterior = produccion
    produccion = is_producing(lista_unos_fondo)
    print("En Produccion: " + str(produccion) + ", Porcentaje de llenado: " + porcentaje)
    i, lista_unos_fondo = inicio_lista()
  
  i+=1
  return i, lista_unos_fondo, prod_frame_anterior, produccion


"""
Empieza el código
"""

"""
Preparo la configuracion del log
"""
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='rejilla.log', filemode='a', format=FORMAT)

cam_url = 'rtsp://10.10.4.151:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA=='
cam_url = './Videos/Videos/2019-11-25 10-15 rejilla1.avi'
#cam_url = './Videos/Videos/2019-11-20 19-13 rejilla5.avi'

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

# Inicializo contador de frames en 2 y la lista vacia
i, lista_unos_fondo = inicio_lista()
# Booleano de en Producción o no comienza en false
produccion = False
prod_frame_anterior = produccion
porcentaje_llenado = "0%"

# Inicializo objeto sustractor de fondo
# Parametros: history, threshold, DetectShadow
mogSub = cv2.createBackgroundSubtractorMOG2(history=15)

#while(get_elapsed_seconds(total_elapsed) < 100):
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    
    k = cv2.waitKey(1)

    # Resize for seeing
    frame = rescale_frame(frame, percent=25)
    blur = cv2.GaussianBlur(frame, (15,15),0)

    # obtengo rejilla entera para aplicarle mask de llenado
    rejilla = get_espacio_llenado(frame)

    # defino espacio detector de movimiento
    movimiento = get_espacio_movimiento(blur)

    i, lista_unos_fondo, prod_frame_anterior, \
      produccion = en_produccion(movimiento, mogSub, i, lista_unos_fondo, produccion, prod_frame_anterior, porcentaje_llenado)

    if produccion:
      """ SE ESTA PRODUCIENDO """
      fecha_hora = get_fecha()
      if not prod_frame_anterior:
        logging.warning("Empezando la produccion")
        print(fecha_hora + " Empezando la produccion")
        prod_frame_anterior = produccion
        print()
      
      # obtengo la mask de llenado con 1s y 0s
      mask = get_silver_mask(rejilla)
      # obtengo porcentaje de 0s y 1s
      porcentaje_unos, porcentaje_ceros = get_porcentaje_color(mask)
      
      porcentaje_llenado = str(int(porcentaje_ceros - 45)) + "%"
      
      # if (porcentaje_unos > 50) and (not wait):
      if not wait and (int(porcentaje_ceros) > 65):
        print("Porcentaje de llenado:")
        print(porcentaje)
        print("Aca deberia haber una alerta con SNS")
        logging.warning("Rejilla comprometida")
        #print(enviar_sms(client, texto="alerta de llenado de rejilla"))
        wait_seconds = time.time()
        wait = True

      if wait and (get_elapsed_seconds(wait_seconds) > 60):
        # Si paso mas de 1 min cuando la bandera de espera era True, ya podemos mandar alertas nuevamente
        wait = False
      
      cv2.imshow('Mask', mask)

      
    if not produccion and prod_frame_anterior:
      # significa que dejo de producir
      fecha_hora = get_fecha()
      logging.warning("Fin de la produccion")
      print(fecha_hora + " Fin de la produccion")
      prod_frame_anterior = produccion
    

    cv2.imshow('frame', frame)
    
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
