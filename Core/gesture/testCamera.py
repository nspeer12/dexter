import cv2
import numpy as np
import socket




class FrameSegment(object):

  MAX_DGRAM = 2**16
  MAX_IMAGE_DGRAM = MAX_DGRAM — 64 # minus 64 bytes in case UDP frame overflown
  
  def __init__(self, sock, port, addr=”127.0.0.1"):
    self.s = sock
    self.port = port
    self.addr = addr

  def udp_frame(self, img):
    compress_img = cv2.imencode(‘.jpg’, img)[1]
    dat = compress_img.tostring()
    size = len(dat)
    num_of_segments = math.ceil(size/(MAX_IMAGE_DGRAM))
    array_pos_start = 0
    
    while num_of_segments:
      array_pos_end = min(size, array_pos_start + MAX_IMAGE_DGRAM)
      self.s.sendto(
                   struct.pack(“B”, num_of_segments) +
                   dat[array_pos_start:array_pos_end], 
                   (self.addr, self.port)
                   )
      array_pos_start = array_pos_end
      num_of_segments -= 1


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 12345
fs = FramSegment(s, port)

print("grabbing camera")
cap = cv2.VideoCapture(0)
print("done")

while True:
    try:
        ret , frame = cap.read(1)
        cv2.imshow('frame',frame)
    except Exception as ex:
        print(ex)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()