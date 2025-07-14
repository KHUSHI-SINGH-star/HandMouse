import cv2 as cv
import mediapipe as mp
import time 


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
    max_num_hands=self.maxHands,
    min_detection_confidence=self.detectionCon,
    min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        RGB_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(RGB_img)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findposition(self,img,handno=0,draw=True):
       lmList=[]
       if self.results.multi_hand_landmarks:
           myhand=self.results.multi_hand_landmarks[handno]
           
           for id,lm in enumerate(myhand.landmark):
                  h,w,c=img.shape
                  cx,cy=int(lm.x*w),int(lm.y*h)
                  lmList.append([id,cx,cy])
                  if draw:

                   if id==8:
                     cv.circle(img,(cx,cy),7,(0,255,0),-1)
                   if id==4:
                      cv.circle(img,(cx,cy),7,(0,255,0),-1)
              

       return lmList 

def main():
    ctime=0
    cap=cv.VideoCapture(0)
    detector = HandDetector(maxHands=2, detectionCon=0.7, trackCon=0.5)
    while True:
      isTrue,img=cap.read()
      img=detector.findHands(img)
      lmList=detector.findposition(img)
      if len(lmList) !=0:
       print(lmList[4])
      ctime=time.time()
      fps=1/(ctime-ptime)
      ptime=ctime
      cv.putText(img,f'FPS:{str(int(fps))}',(10,70),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
      cv.putText(img,'Press "d" to exit',(10,30),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
      

      cv.imshow('img',img)
      if cv.waitKey(1) & 0xFF==ord('d'):
        break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()