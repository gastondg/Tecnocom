import cv2
import numpy as np
from datetime import datetime

# Create a VideoCapture object
#cap = cv2.VideoCapture('rtsp://admin:tecno20@10.10.4.152:554/cam/realmonitor?channel=1&subtype=1')
cap = cv2.VideoCapture("http://10.10.4.152/axis-cgi/mjpg/video.cgi?camera=2")


# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_width, frame_height)
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy152.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
       20, (frame_width, frame_height)) 
#out = cv2.VideoWriter('outpy152-1080p.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
#                      15, (1920, 1080))

# fecha inicio
a = datetime.now()
while(True):
  ret, frame = cap.read()

  if ret == True:

    # Write the frame into the file 'output.avi'
    out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # controlo segundos pasados
    b = datetime.now()
    c = b-a
    if int(c.seconds) == 20:
      break
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

# When everything done, release the video capture and video write objects
cap.release()
#out.release()

# Closes all the frames
cv2.destroyAllWindows()
