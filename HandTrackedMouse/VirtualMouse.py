import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

widthCam, heightCam  = 648 , 488
frameReduction = 100
smoothening = 5
PrevLocX, PrevLocY = 0,0
CurLocX, CurLocY = 0,0
widthScreen, heightScreen = autopy.screen.size()
cap = cv2.VideoCapture(1)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0
detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    CV2.rectangle(img,(frameReduction,frameReduction),(widthCam-frameReduction,heightCam-frameReduction),(255,0,255),2)
    
    if len(lmList) != 0 :
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        print(fingers)

        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameReduction, widthCam-frameReduction), (0, widthScreen))
            y3 = np.interp(x1, (frameReduction, heightCam-frameReduction), (0, heightScreen))
            CurLocX = PrevLocX + (x3 - PrevLocX)// smoothening
            CurLocY = PrevLocY + (x3 - PrevLocY)// smoothening

            autopy.mouse.move(widthScreen-CurLocX,CurLocY)
            cv2.circle(img,(x1,y1),15,(255,255,0),cv2.FILLED)

        if fingers[1] == 1 and fingers[2] == 1:
            length,img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length<40:
                cv2.circle(img,(lineInfo[4], lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()



    cTime = time.time()
    fps = 1/(ctime - pTime)
    ptime = cTime 
    cv2.putText(img, str(int(fps)),(28,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

