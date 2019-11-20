import cv2 
import numpy as np

cap = cv2.VideoCapture('./Videos/Videos/2019-11-05 16-18 enfriamiento1.avi')
print("Analizando " + arch)
print()

 while cap.isOpened():
     # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    
        k = cv2.waitKey(1)

        frame = cv2.pyrDown(frame)
        frame = cv2.pyrDown(frame)

        # Convierto a gris
        gray = cv2.cvtColor(frame, )


        cv2.imshow("Frame",frame)

        if k == ord('q'):
            break