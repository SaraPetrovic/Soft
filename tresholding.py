import cv2
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
print("HEIGHT " + repr(height)) #480
print("WIDTH " + repr(width)) #640

#define range of blue color in HSV
BLUE_MIN = np.array([98, 109, 20], np.uint8)
BLUE_MAX = np.array([112, 255, 255], np.uint8)

centroid_x = 0
centroid_y = 0

while(cap.isOpened()):

    ret, img = cap.read()
    img = cv2.flip(img, 1)

   
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frame_threshed = cv2.inRange(hsv, BLUE_MIN, BLUE_MAX)

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #_, frame_threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours,hierarchy = cv2.findContours(frame_threshed, 1, 2)

    max_area = 0
    if contours:
        for i in contours:
            area = cv2.contourArea(i)
            if area > max_area:
                max_area = area
                contour = i

        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        centroid_x = int((x + x+w)/2)
        centroid_y = int((y + y+h)/2)
        
        cv2.circle(img, (centroid_x, centroid_y), 2, (0,0,255), 2)
        cv2.line(img,(150,0),(150,700),(255,0,0),5)
        cv2.line(img,(450,0),(450,700),(255,0,0),5)
        cv2.line(img,(150,240),(450, 240),(255,0,0),5)

        #cv2.imshow('HSV', hsv)
        #cv2.imshow('Threshold', frame_threshed)
        cv2.imshow('Original', img)


        # up-down move
        if centroid_x >= 200 and centroid_x <= 400:
            if centroid_y >= 0 and centroid_y <= 240:
                print ('up')
                pyautogui.press('up')
            if centroid_y >= 240 and centroid_y <=480:
                print ('down')
                pyautogui.press('down')

        # left-right move
        if centroid_y >= 0 and centroid_y <= 480:
            if centroid_x >= 0 and centroid_x <= 150:
                print ('left')
                pyautogui.press('left')
            if centroid_x >= 450:
                print ('right')
                pyautogui.press('right')


    k = cv2.waitKey(10)
    if k == 27:
        break
 
