import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Get the location of the Point Numbers of the Hand (initiate)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity , self.detectionCon, self.trackCon)
        # draw lines between hands (initiate)
        self.mpDraw = mp.solutions.drawing_utils
    

    def findHands(self, img, draw=True):
        # send in rbg image to object (convert to RGB img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # process frame --> result
        self.results = self.hands.process(imgRGB)
        # extract information out of object (check for identified hands and eliminate multiple detected hands)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # draw lines and points on original image
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img


    def findPosition(self, img, handNo=0, draw=True):
        
        # initialize Landmark List which will be returned
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            # identifying landmarks on hand and transform it to pixel coordinates + mark them
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                # identify a special landmark and mark it with a circle
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)
        
        return lmList



def main():

    # initialize previous  and current time
    pTime = 0
    cTime = 0
    cap = cv2. VideoCapture(1)

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)

        # getting Landmark List from function
        lmList = detector.findPosition(img)
        # if len(lmList) != 0:
        #     print(lmList[4])

        # show FPS Numbers
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        img = cv2.flip(img, 1)
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        
        
        cv2.imshow("Image", img)
        # cv2.waitKey(1)
        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            print("quit")
            break
        

if __name__ == "__main__":
        main()