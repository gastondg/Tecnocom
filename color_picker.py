import cv2
import numpy as np


class ColorPicker():        

    def __init__(self):
        cv2.namedWindow("hsv_picker")
        # defino lower
        cv2.createTrackbar("Low H", "hsv_picker", 0, 255, self.nothing)
        cv2.createTrackbar("Low S", "hsv_picker", 0, 255, self.nothing)
        cv2.createTrackbar("Low V", "hsv_picker", 0, 255, self.nothing)
        # defino upper
        cv2.createTrackbar("Up H", "hsv_picker", 255, 255, self.nothing)
        cv2.createTrackbar("Up S", "hsv_picker", 255, 255, self.nothing)
        cv2.createTrackbar("Up V", "hsv_picker", 255, 255, self.nothing)

    def nothing(self, x):
        pass

    def pick_color(self, img):
        """ Creamos el TrackBar y elegimos el color
            img debe ser HSV!
        """
        low_h = cv2.getTrackbarPos("Low H", "hsv_picker")
        low_s = cv2.getTrackbarPos("Low S", "hsv_picker")
        low_v = cv2.getTrackbarPos("Low V", "hsv_picker")

        up_h = cv2.getTrackbarPos("Up H", "hsv_picker")
        up_s = cv2.getTrackbarPos("Up S", "hsv_picker")
        up_v = cv2.getTrackbarPos("Up V", "hsv_picker")

        """ lower_color = np.array([low_h, low_s, low_v])
        upper_color = np.array([up_h, up_s, up_v]) """
        
        lower_color = (low_h, low_s, low_v)
        upper_color = (up_h, up_s, up_v)
        
        return lower_color, upper_color


