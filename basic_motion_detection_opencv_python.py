import cv2
import numpy as np
import matplotlib.pyplot as plt


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
    
cap = cv2.VideoCapture('./Videos/Videos/2019-11-05 16-18 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/2019-11-15 10-07 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/2019-11-13 12-54 enfriamiento1.avi')
#cap = cv2.VideoCapture('./Videos/Videos/1 -  enfriamiento.avi')


# Parametros: history, threshold, DetectShadow
mogSub = cv2.createBackgroundSubtractorMOG2()
#KNNSub = cv2.createBackgroundSubtractorKNN()

band = True
x, y, w, h = 116, 407, 677, 133
# Listas
unos_mog = []
unos_knn = []

while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    
        k = cv2.waitKey(1)

        # Resize para verlo
        #frame = rescale_frame(frame, percent=20)
        frame = cv2.pyrDown(frame)
        frame = cv2.pyrDown(frame)
        
        frame = cv2.GaussianBlur(frame, (5,5),0)
        frame = cv2.medianBlur(frame, 5)

        # Seleccionamos la ROI presionando "r" en el teclado
        if  k == ord('r'):
            # obtengo la roi
            x, y, w, h = cv2.selectROI("Frame", frame, False, False)
            print("ROI: ")
            print(x, y, w, h)
            band = True

        if band: # esta seleccionada la ROI
            
            corte = frame[y:y+h, x:x+w]

            # Remuevo el fondo
            mask_mog = mogSub.apply(corte)
            #mask_knn = KNNSub.apply(corte)

            # añado los unos que encuentra
            unos_mog.append(np.count_nonzero(mask_mog)) 
            #unos_knn.append(np.count_nonzero(mask_knn))

            #print("Unos MOG: {}".format(np.count_nonzero(mask_mog)))
            #print("Unos KNN: {}".format(np.count_nonzero(mask_knn)))

            #cv2.imshow("KNN Mask",mask_knn)
            cv2.imshow("MOG2 Mask",mask_mog)
        
        cv2.imshow("Frame",frame)

       # diff = cv2.absdiff(frame, mask_sustracted)
       # cv2.imshow(diff)

        if k == ord('q'):
            break
    else:
        break 
        #cap = cv2.VideoCapture('./Videos/Videos/1 -  enfriamiento.avi')

# Una vez que salimos hacemos un analisis
if unos_knn:    
    print("Analisis de KNN")
    print(analisis(unos_knn))
if unos_mog:
    print("Analisis de MOG2")
    print(analisis(unos_mog))

cv2.destroyAllWindows()
cap.release()
