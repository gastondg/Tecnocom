import cv2
import numpy as np
import time
import multiprocessing
import zipfile

def get_elapsed_seconds(start):
  # devuelve el tiempo transcurrido, en segundos
  return int(time.time() - start)

def comprimir_video(filename, out):
  """ Recibe nombre del video y el object OUT con el video """
  out.release()
  zip_file = zipfile.ZipFile(filename.replace(".avi", ".zip"), 'w')
  zip_file.write(filename, compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()

def get_nuevo_vid(cam_url, filename, frame_width, frame_height):
  """ Devuelve un nuevo cv2 writer de video """
  out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),\
      15, (frame_width, frame_height))
  cap = cv2.VideoCapture(cam_url)
  return cap, out

cam_url = 'rtsp://10.10.4.151:554/cam/realmonitor?channel=1&subtype=0&authbasic=YWRtaW46dGVjbm8yMA=='
# cam_url = 0
# Create a VideoCapture object
cap = cv2.VideoCapture(cam_url)

# Check if camera opened successfully
if (cap.isOpened() == False):
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_width, frame_height)

# fecha inicio
i = 1

filename = "video151-{}.avi"
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
cap, out = get_nuevo_vid(cam_url,filename.format(i), frame_width, frame_height)

start = time.time()
total_elapsed = time.time()q
while(get_elapsed_seconds(total_elapsed) < 43000):
  ret, frame = cap.read()

  if ret == True:

    # Write the frame into the file 'output.avi'
    out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    if int(get_elapsed_seconds(start)) >= 300:
      # pasaron 5 min -> grabo el video y lo comprimo
      """ p = multiprocessing.Process(target=comprimir_video, args=[filename.format(i), out])
      p.start() """
      out.release()
      cap.release()
      i += 1
      cap, out = get_nuevo_vid(cam_url,filename.format(i), frame_width, frame_height)
      start = time.time()

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

  

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
