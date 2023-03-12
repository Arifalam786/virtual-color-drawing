import cv2
import numpy as np

cap = cv2.VideoCapture(1)    # 0 use default web camera
cap.set(3,640)       # width id no 3 as 640
cap.set(4,480)       # height id no 4 as 480
cap.set(10,100)      # brightness id no 10 as 100
myColors = [[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255],[90,48,0,118,255,255],[0,77,181,179,255,255]]
myColorsValues = [[51,153,255],[255,0,255],[0,255,0],[255,0,0],[0,255,255]]       #BGR
myPoints = []  #[x,y,colorId]

def findColor(img,myColors,myColorsValue):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorsValue[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)   #imgContour, cnt, index for printing all, color, thickness
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)      # to check the corner points
            x, y, w, h = cv2.boundingRect(approx)    #creating boundary of each objects
    return x+w//2,y


def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorsValues[point[2]],cv2.FILLED)


while True:
    success, img  = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorsValues)
    #print(newPoints)
    
    if len(newPoints)!=0:
        for newp in newPoints:
            myPoints.append(newp)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorsValues)
    #print(myPoints)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break