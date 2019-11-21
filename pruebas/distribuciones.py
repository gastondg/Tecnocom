import cv2
import numpy as np
from color_picker import ColorPicker
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab

def show_hist(array):
  pass


def nothing(x):
  pass

def pick_color(img):
  """ Creamos el TrackBar y elegimos el color
      img debe ser HSV!
  """
  cv2.namedWindow("hsv_picker")
  # defino lower
  cv2.createTrackbar("Low H", "hsv_picker", 0, 255, nothing)
  cv2.createTrackbar("Low S", "hsv_picker", 0, 255, nothing)
  cv2.createTrackbar("Low V", "hsv_picker", 0, 255, nothing)
  # defino upper
  cv2.createTrackbar("Up H", "hsv_picker", 255, 255, nothing)
  cv2.createTrackbar("Up S", "hsv_picker", 255, 255, nothing)
  cv2.createTrackbar("Up V", "hsv_picker", 255, 255, nothing)

  low_h = cv2.getTrackbarPos("Low H", "hsv_picker")
  low_s = cv2.getTrackbarPos("Low S", "hsv_picker")
  low_v = cv2.getTrackbarPos("Low V", "hsv_picker")

  up_h = cv2.getTrackbarPos("Up H", "hsv_picker")
  up_s = cv2.getTrackbarPos("Up S", "hsv_picker")
  up_v = cv2.getTrackbarPos("Up V", "hsv_picker")

  lower_color = np.array([low_h, low_s, low_v])
  upper_color = np.array([up_h, up_s, up_v])
  
  return lower_color, upper_color

def rescale_frame(frame, percent=75):
    scale_percent = percent / 100
    width = int(frame.shape[1] * scale_percent )
    height = int(frame.shape[0] * scale_percent )
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def select_roi(img):
    r = cv2.selectROI("Image", img, False, False)
    # return x, y, w, h = roi
    return r

def select_mask(frame):
    """ Elegimos el color y devolvemos con la mask """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #color_picker = ColorPicker()
    #lower_color, upper_color = color_picker.pick_color(hsv)
    lower_color = (105,10,100)
    upper_color = (115,40,255)
    
    mask = cv2.inRange(hsv, lower_color, upper_color)

    return mask

def get_silver_mask(frame):
  """ Devolvemos la silver mask """
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask1 = cv2.inRange(hsv, (150,3,210), (170,40,255))
  mask2 = cv2.inRange(hsv, (110,0,100), (130,40,200))
  mask3 = cv2.inRange(hsv, (8,12,140), (28,26,255))
  #mask4 = cv2.inRange(hsv, (10,5,95), (30,40,255))
  mask = cv2.inRange(hsv, (105,0,80), (115,50,255))
  #mask = mask1+mask2+mask3
  
  return mask

def get_range(corte):
  """ Retorna los limites de la mask """
  h,s,v = cv2.split(corte)
  h_med = np.median(h)
  s_max = s.max()
  s_min = s.min()
  v_max = v.max()
  v_min = v.min()
  lower_color = (h_med-10, s_min, v_min)
  upper_color = (h_med+10, s_max, v_max)
  
  return lower_color, upper_color

# Leer el archivo
#cap = cv2.VideoCapture('./Videos/Videos/10-22-2019 16-09 con luz led de punta de linea.avi')
cap = cv2.VideoCapture('./Videos/Videos/2019-11-20 19-13 rejilla5.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

cv2.namedWindow("hsv_picker")
# defino lower
cv2.createTrackbar("Low H", "hsv_picker", 0, 255, nothing)
cv2.createTrackbar("Low S", "hsv_picker", 0, 255, nothing)
cv2.createTrackbar("Low V", "hsv_picker", 0, 255, nothing)
# defino upper
cv2.createTrackbar("Up H", "hsv_picker", 255, 255, nothing)
cv2.createTrackbar("Up S", "hsv_picker", 255, 255, nothing)
cv2.createTrackbar("Up V", "hsv_picker", 255, 255, nothing)

band = False

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    
    k = cv2.waitKey(1)

    # Resize for seeing
    frame = rescale_frame(frame, percent=25)

    # Seleccionamos la ROI presionando "r" en el teclado
    if  k == ord('r'):
        # obtengo la roi
        x, y, w, h = cv2.selectROI("Cam", frame, False, False)
        print("ROI: ")
        print(x, y, w, h)
        band = True

    if band:
      corte = frame[y:y+h, x:x+w]
      #hsv = cv2.cvtColor(corte, cv2.COLOR_BGR2HSV)
      corte = cv2.cvtColor(corte, cv2.COLOR_BGR2HSV)
      #h1,s,v = cv2.split(corte)
      #print(h1)
      #hist = cv2.calcHist([corte],[0],None,[256],[0,256])
      #plt.plot(hist)
      #plt.show()
      #band= False
      


      low_h = cv2.getTrackbarPos("Low H", "hsv_picker")
      low_s = cv2.getTrackbarPos("Low S", "hsv_picker")
      low_v = cv2.getTrackbarPos("Low V", "hsv_picker")

      up_h = cv2.getTrackbarPos("Up H", "hsv_picker")
      up_s = cv2.getTrackbarPos("Up S", "hsv_picker")
      up_v = cv2.getTrackbarPos("Up V", "hsv_picker")

      lower_color = np.array([low_h, low_s, low_v])
      upper_color = np.array([up_h, up_s, up_v])

      mask = cv2.inRange(corte, lower_color, upper_color)
      res = cv2.bitwise_not(frame[y:y+h, x:x+w], frame[y:y+h, x:x+w], mask=mask)

      cv2.imshow("Mask", mask)
      cv2.imshow("Result", res)
            
      #band = False
    

    cv2.imshow("Cam", frame)
    
    # Press Q on keyboard to  exit
    if k == ord('q'):
      break
 
  # Break the loop
  else:
    cap = cv2.VideoCapture('./Videos/Videos/2019-11-20 19-13 rejilla5.avi')

    #cap = cv2.VideoCapture('./Videos/Videos/2019-11-01 12-30 rejilla1.avi')
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()