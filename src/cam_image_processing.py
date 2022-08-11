import cv2
import numpy as np
import socket

cam_ip = 'http://192.168.0.27:81/stream'
servo_server_ip = '127.0.0.1'
servo_server_port = 12345

s = socket.socket()
s.connect((servo_server_ip, servo_server_port))
camera_stream = cv2.VideoCapture(cam_ip)

lowerBlue = 50
lowerGreen = 20
lowerRed = 20

upperBlue = 100
upperGreen = 255
upperRed = 255

window_name = "Cam"

vid_available, img = camera_stream.read()

def nothing(xOffset):
    pass

cv2.imshow(window_name, img)

def createSliders():
    cv2.createTrackbar("Lower Blue", window_name, 0, 255, nothing)
    cv2.createTrackbar("Lower Green", window_name, 0, 255, nothing)
    cv2.createTrackbar("Lower Red", window_name, 0, 255, nothing)

    cv2.createTrackbar("Upper Blue", window_name, 0, 255, nothing)
    cv2.createTrackbar("Upper Green", window_name, 0, 255, nothing)
    cv2.createTrackbar("Upper Red", window_name, 0, 255, nothing)

    cv2.setTrackbarPos("Lower Blue", window_name, 0)
    cv2.setTrackbarPos("Lower Green", window_name, 0)
    cv2.setTrackbarPos("Lower Red", window_name, 0)
    cv2.setTrackbarPos("Upper Blue", window_name, 255)
    cv2.setTrackbarPos("Upper Green", window_name, 255)
    cv2.setTrackbarPos("Upper Red", window_name, 255)

def readSliders():
    global lowerBlue
    global lowerGreen
    global lowerRed
    global upperBlue
    global upperGreen
    global upperRed

    lowerBlue = cv2.getTrackbarPos("Lower Blue", window_name)
    lowerGreen = cv2.getTrackbarPos("Lower Green", window_name)
    lowerRed = cv2.getTrackbarPos("Lower Red", window_name)

    upperBlue = cv2.getTrackbarPos("Upper Blue", window_name)
    upperGreen = cv2.getTrackbarPos("Upper Green", window_name)
    upperRed = cv2.getTrackbarPos("Upper Red", window_name)

createSliders()

width = int(camera_stream.get(3))
height = int(camera_stream.get(4))

print(width)
print(height)

center_point = (int(width / 2), int(height / 2))

running = True

while running:
    vid_available, img = camera_stream.read()

    if vid_available:

        readSliders()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([lowerBlue, lowerGreen, lowerRed])   
        upper_bound = np.array([upperBlue, upperGreen, upperRed])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        kernel = np.ones((7,7),np.uint8)

        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        segmented_img = cv2.bitwise_and(img, img, mask=mask)

        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.circle(img, center_point, 10, (0, 255, 0), -1)

        for i in contours:
            M = cv2.moments(i)
            area = M['m00']
            if area > 5000:
                cx = int(M['m10']/area)
                cy = int(M['m01']/area)
                cv2.circle(img, (cx, cy), 8, (0, 0, 255), -1)
                cv2.line(img, center_point, (cx, cy), (0, 255, 0), 5)

                offset = (round(-(center_point[0] - cx) / center_point[0], 2), round((center_point[1] - cy) / center_point[1], 2))

                offset_text = ','.join((str(offset[0]), str(offset[1])))

                s.send(offset_text.encode())

                text = ','.join((offset_text, str(area)))
                cv2.putText(img, text, (cx, cy),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                

        output = cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
        
        cv2.imshow(window_name, output)

    if ord('q')==cv2.waitKey(10):
        s.close()
        exit(0)
        