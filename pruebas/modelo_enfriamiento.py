import cv2
import numpy as np
from datetime import datetime

def rescale_frame(frame, percent=75):
    scale_percent = percent / 100
    width = int(frame.shape[1] * scale_percent )
    height = int(frame.shape[0] * scale_percent )
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def unos_blur(blur, x, y, h, w, mogSub):
     
    corte = blur[y:y+h, x:x+w]
    # Remuevo el fondo
    mask_mog = mogSub.apply(corte)
    # devuelvo unos que encuentra
    return np.count_nonzero(mask_mog)
     
def is_producing(lista):
    
    list = np.array(lista)
    minimo = list.min()
    print()
    print("Minimo de la lista: " + str(minimo))
    if minimo > 500:
        return True
    return False

# Leer el archivo
cap = cv2.VideoCapture('./Videos/Videos/2019-11-20 19-13 enfriamiento5.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Booleano de en Producción o no comienza en false
produccion = False
prod_frame_anterior = produccion
# enfriamiento
x, y, w, h = 116, 407, 677, 133
# rejilla
#x, y, w, h = 115, 193, 618, 267

# Inicializo contador de frames en 2 
i=2
lista_unos_fondo = []

# Inicializo objeto sustractor de fondo
# Parametros: history, threshold, DetectShadow
mogSub = cv2.createBackgroundSubtractorMOG2(history=15)

# Read until video is completed
while(cap.isOpened()):
    # Capturamos frame-por-frame
    ret, frame = cap.read()
    # Si agarra un frame
    if ret == True:

        k = cv2.waitKey(1)
        # Presionamos Q en el teclado para salir
        if k == ord('q'):
            break
        
        # Resize y blur para analisis y visualizacion 
        blur = cv2.pyrDown(frame)
        blur = cv2.pyrDown(blur)
        blur = cv2.GaussianBlur(blur, (15,15),0)
        #blur = cv2.medianBlur(blur, 5)
        frame = rescale_frame(frame, percent=25)
        
        # Dibujo el rectangulo
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2) 

        # Agrego unos a la lista
        unos_blur_v = unos_blur(blur, x, y, h, w, mogSub)
        lista_unos_fondo.append(unos_blur_v)

        # actualizo booleano anterior

        if i % 75 == 0:
            prod_frame_anterior = produccion
            produccion = is_producing(lista_unos_fondo)
            print("Produccion: " + str(produccion))
            i = 2
            lista_unos_fondo = []
        i+=1
        """print(i, lista_unos_fondo)"""
        
        if produccion:
            
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

            if not prod_frame_anterior:
                print("Empezando la produccion " + fecha_hora)
                prod_frame_anterior = produccion
                print()
            
        if not produccion and prod_frame_anterior:
            # significa que dejo de producir
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            print("Fin de la produccion " + fecha_hora)
            prod_frame_anterior = produccion


        cv2.imshow("Frame",frame)
        cv2.imshow("Blur",blur)
    # Break the loop
    else:
        cap = cv2.VideoCapture('./Videos/Videos/2019-11-20 19-13 enfriamiento5.avi')
        #break
cv2.destroyAllWindows()
cap.release()

    