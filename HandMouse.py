import cv2 as cv
import time
import hand_traking as ht
import pyautogui as py
import datetime
import keyboard




screen_width, screen_height = py.size()

def findposition_modified(img, results, handno=0, draw=True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handno]


        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])


            if draw:
                if id == 8:
                    mouse_x = int(screen_width / w * cx)
                    mouse_y = int(screen_height / h * cy)
                    py.moveTo(mouse_x, mouse_y)
                    x1 = cx
                    y1 = cy
                    # cv.circle(img, (cx, cy), 7, (0, 255, 0), -1)
                if id == 4:
                    x2 = cx
                    y2 = cy
                    # cv.circle(img, (cx, cy), 7, (0, 255, 0), -1)

        index_finger_up = myHand.landmark[8].y < myHand.landmark[6].y
        middle_finger_up = myHand.landmark[12].y < myHand.landmark[10].y
        ring_finger_up = myHand.landmark[16].y < myHand.landmark[14].y
        pinky_finger_up = myHand.landmark[20].y < myHand.landmark[18].y

        open_fingers = sum([index_finger_up, middle_finger_up, ring_finger_up, pinky_finger_up])
        
        if open_fingers == 2 and index_finger_up and middle_finger_up:
           py.doubleClick()
           print("Double Clicked")
           time.sleep(1) 

        elif open_fingers == 1 and index_finger_up:
            py.click()
            print("Clicked")
            time.sleep(1) 

        
        elif open_fingers == 4:
            dist = y2 - y1
            print(f"Distance: {dist}")
            # cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        

            if 40 < dist <= 60:
                keyboard.send("volume up")
                print("Volume Up")
                time.sleep(1)

            elif 20 < dist <= 35:
                keyboard.send("volume down")
                print("Volume Down")
                time.sleep(1)

            elif dist < 10:
                filename = datetime.datetime.now().strftime("screenshot_%Y-%m-%d_%H-%M-%S.png")
                py.screenshot(filename)
                print(f"Screenshot saved as {filename}")
                time.sleep(1)


    return lmList

def main():
    ptime=0
    ctime=0
    cap=cv.VideoCapture(0)
    detector = ht.HandDetector(maxHands=2, detectionCon=0.7, trackCon=0.5)
    while True:
      isTrue,img=cap.read()
      img=detector.findHands(img)
      lmList=detector.findposition(img)
      results = detector.results
      lmList = findposition_modified(img, results)
 
      ctime=time.time()
      fps=1/(ctime-ptime)
            
      ptime=ctime
      img=cv.flip(img,1)

      cv.putText(img,f'FPS:{str(int(fps))}',(10,70),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
      cv.putText(img,'Press "d" to exit',(10,30),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
      cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
      cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
 
      cv.imshow('img',img)
      if cv.waitKey(50) & 0xFF==ord('d'):
        break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()