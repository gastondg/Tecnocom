import cv2 
import numpy as np


nombre= "2019-11-05 16-04 rejilla1.avi"
cap = cv2.VideoCapture('./Videos/Videos/' + nombre)
print("Analizando " + nombre)
print()

band = False

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    
        k = cv2.waitKey(1)

        frame = cv2.pyrDown(frame)
        frame = cv2.pyrDown(frame)
        
        if  k == ord('r'):
            # obtengo la roi
            x, y, w, h = cv2.selectROI("Frame", frame, False, False)
            print("ROI: ")
            print(x, y, w, h)
            band = True
        
        if band: # esta seleccionada la ROI
            corte = frame[y:y+h, x:x+w]
            # Convierto a gris
            gray = cv2.cvtColor(corte, cv2.COLOR_BGR2GRAY)

            edges = cv2.Canny(gray, 50, 200 )
            lines = cv2.HoughLinesP(edges,1, np.pi/90,200)
            if lines.any():
                    
                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    cv2.line(gray, (x1,y1), (x2,y2), (0,0,255), 1)
                #cv2.imshow("Edges",edges)
                gray = cv2.pyrUp(gray)
                cv2.imshow("Gray",gray)




        cv2.imshow("Frame",frame)

        if k == ord('q'):
            break