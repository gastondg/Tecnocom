import cv2
import numpy as np
from color_picker import ColorPicker

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
    scale_percent = percent
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
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
    
    """ lower_color = (150,0,200)
    upper_color = (150,10,255)
    
    mask2 = cv2.inRange(hsv, lower_color, upper_color)

    mask = mask + mask2 """

    return mask

# Leer el archivo
cap = cv2.VideoCapture('../Videos/outpy151.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
band = False

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    
    k = cv2.waitKey(1)

    # Resize for seeing
    frame = rescale_frame(frame, percent=40)

    # Seleccionamos la ROI presionando "r" en el teclado
    if  k == ord('r'):
        # obtengo la roi
        x, y, w, h = cv2.selectROI("Cam", frame, False, False)
               
        band = True

    if band:
      # esta seleccionada la ROI
      corte = frame[y:y+h, x:x+w]
      # obtengo la mask eligiendo el color
      mask = select_mask(corte)
      mask_inv = cv2.bitwise_not(mask)
      cv2.imshow("Mask", mask)
      cv2.imshow("Mask Invertida", mask_inv)
    

    cv2.imshow("Cam", frame)
    
    # Press Q on keyboard to  exit
    if k == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()