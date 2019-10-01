import cv2
import numpy as np
import time

caps = ['rtsp://10.10.4.152:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA==',
        'rtsp://10.10.4.151:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA==']

filename = "outpy152.avi"
for cap in caps:
  # Create a VideoCapture object
  cap = cv2.VideoCapture(cap)
  #cap = cv2.VideoCapture("http://10.10.4.151/axis-cgi/mjpg/video.cgi?camera=0")


  # Check if camera opened successfully
  if (cap.isOpened() == False):
    print("Unable to read camera feed")

  # Default resolutions of the frame are obtained.The default resolutions are system dependent.
  # We convert the resolutions from float to integer.
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))
  print(frame_width, frame_height)
  # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
  
  out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
        15, (frame_width, frame_height)) 
  #out = cv2.VideoWriter('outpy152-1080p.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
  #                      15, (1920, 1080))

  # fecha inicio
  i = 1
  filename = "video151-{}.avi"
  start = time.time()
  while(True):
    ret, frame = cap.read()

    if ret == True:

      # Write the frame into the file 'output.avi'
      out.write(frame)

      # Display the resulting frame
      cv2.imshow('frame', frame)
      
      # controlo segundos pasados
      end = time.time()
      seconds_elapsed = end - start
      if int(seconds_elapsed) >= 300:
        break
      # Press Q on keyboard to stop recording
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Break the loop
    else:
      break

  # When everything done, release the video capture and video write objects
  cap.release()
  filename = "outpy151.avi"
  #out.release()

  # Closes all the frames
  cv2.destroyAllWindows()
