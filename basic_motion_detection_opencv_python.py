import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import os


def rescale_frame(frame, percent=75):
    scale_percent = percent / 100
    width = int(frame.shape[1] * scale_percent )
    height = int(frame.shape[0] * scale_percent )
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def reject_outliers(data, m=6):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def analisis(lista):
    """ La lista contiene la cuenta de unos en la mask por cada frame """
    print("Maximo de unos: {}".format(max(lista)))
    print("Minimo de unos: {}".format(min(lista)))
    lista = np.asarray(lista)
    print("Promedio de unos: {}".format(np.mean(lista)))
    print("Mediana de unos: {}".format(np.median(lista)))
    lista = reject_outliers(lista)
    plt.hist(lista)
    plt.show()
    return

def to_csv(lista, nombre):
    """ Graba todo a csv """
    with open(nombre, 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(lista)
    return "Terminado " + nombre
    
#cap = cv2.VideoCapture('./Videos/Videos/2019-11-05 16-18 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/2019-11-15 10-07 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/2019-11-13 12-54 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/1 -  enfriamiento.avi')
cap = cv2.VideoCapture('./Videos/Videos/2019-11-19 10-21 rejilla1.avi')

#for arch in os.listdir("./Videos/Videos"):
    #if "enfriamiento" in arch:
        #cap = cv2.VideoCapture("./Videos/Videos/"+arch)
        #print("Analizando " + arch)
        #print()

# Parametros: history, threshold, DetectShadow
mogSub = cv2.createBackgroundSubtractorMOG2(history=15)
#KNNSub = cv2.createBackgroundSubtractorKNN()

band = True
# enfriamiento
#x, y, w, h = 116, 407, 677, 133
# rejilla
x, y, w, h = 90, 74, 678, 223

# Listas
unos_mog = []

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    
        k = cv2.waitKey(1)


        # Resize para verlo
        blur = cv2.pyrDown(frame)
        blur = cv2.pyrDown(blur)
        blur = cv2.GaussianBlur(blur, (15,15),0)
        #blur = cv2.medianBlur(blur, 5)
        frame = rescale_frame(frame, percent=25)
        
        # Dibujo el rectangulo
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2) 
        
        # Seleccionamos la ROI presionando "r" en el teclado
        """if  k == ord('r'):
            # obtengo la roi
            x, y, w, h = cv2.selectROI("Frame", frame, False, False)
            print("ROI: ")
            print(x, y, w, h)
            band = True"""

        if  k == ord('r'):
            # obtengo la roi
            x, y, w, h = cv2.selectROI("Frame", frame, False, False)
            print("ROI: ")
            print(x, y, w, h)
            band = True

        if band: # esta seleccionada la ROI
            
            corte = blur[y:y+h, x:x+w]

            # Remuevo el fondo
            mask_mog = mogSub.apply(corte)

            # añado los unos que encuentra
            unos_mog.append(np.count_nonzero(mask_mog)) 

            #cv2.imshow("KNN Mask",mask_knn)
            cv2.imshow("MOG2 Mask",mask_mog)
        
        cv2.imshow("Frame",frame)
        cv2.imshow("Blur",blur)

    # diff = cv2.absdiff(frame, mask_sustracted)
    # cv2.imshow(diff)

        if k == ord('q'):
            break
    else:
        break 
        #cap = cv2.VideoCapture('./Videos/Videos/1 -  enfriamiento.avi')

# Una vez que salimos hacemos un analisis
if unos_mog:
    nombre = "2019-11-19 10-21 rejilla1.csv"
    #nombre = arch.replace(".avi", ".csv")
    to_csv(unos_mog, nombre)

cv2.destroyAllWindows()
cap.release()
