import cv2 
import cvzone
import time 
import HandTrackingModule as h_mod
import mediapipe as mp
import random
import numpy as np

while True:
    cap = cv2.VideoCapture(1)
    # set video frame width to 640px
    cap.set(3, 1080)
    # set video frame height to 640px
    cap.set(4, 720)
    # initialize Hand Detector
    detector = h_mod.HandDetector(maxHands=1)
    # initialize timer
    timer = 0
    # initialize state
    stateResult = False
    # initialize flag
    startGame = False
    # initialize Score
    scores = [0,0] # [AI Score, Player Score]
    # initialize Fair Mode (random AI Move)
    fairMode = True


    while True:
        # background img
        imgBG = cv2.imread("Resources/BG2.png")

        success, img = cap.read()
        height = np.size(img, 0)
        width = np.size(img, 1)
        # print([width, height])
        if width==1920:
            break  

        # resize img to fit in Background box (640x755) #(640x750)
        imgScaled = cv2.resize(img, (0,0), None, 1.0417, 1.0417)
        imgScaled = imgScaled[:,220:860]
        # flip image
        imgScaled = cv2.flip(imgScaled, 1)

        # Find Hands
        hands, img = detector.findHands(imgScaled)
        # Game
        if startGame:
            if stateResult is False:
                timer = time.time() - initialTime
                cv2.putText(imgBG, str(int(timer)), (1060, 1000), cv2.FONT_HERSHEY_PLAIN, 13, (255,0,0), 10)
                
                if timer>3:
                    stateResult = True
                    timer = 0

                    if hands:
                        hand = hands[0]
                        playerMove = None
                        fingers = detector.fingersUp(hand)
                        # Check Player moves
                        if fingers == [0,0,0,0,0] or fingers == [1,0,0,0,0]:
                            playerMove = 1 # Rock
                        if fingers == [1,1,1,1,1] or fingers == [0,1,1,1,1]:
                            playerMove = 2 # Paper
                        if fingers == [0,1,1,0,0] or fingers == [1,1,1,0,0]:
                            playerMove = 3 # Scissors
                        
                        # Generate AI Move
                        if fairMode:
                            AIMove = random.randint(1,3) # random Int (1,2,3)
                        else:
                            if playerMove==1:
                                AIMove = 2
                            elif playerMove==2:
                                AIMove = 3
                            else:
                                AIMove = 1
                        moves = [playerMove, AIMove]
                        imgAI = cv2.imread(f'Resources/{AIMove}.png', cv2.IMREAD_UNCHANGED)
                        imgAI = cv2.resize(imgAI, (0,0), None, 2, 2)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (300,700))
                        
                        # Check if Player or AI won
                        # Player wins
                        if moves==[1,3] or moves==[2,1] or moves==[3,2]:
                            scores[1]+=1
                        # AI wins
                        if moves==[1,2] or moves==[2,3] or moves==[3,1]:
                            scores[0]+=1
                        # print(moves)
                        # print(scores)
                    else:
                        imgAI = cv2.imread(f'Resources/0.png', cv2.IMREAD_UNCHANGED)
                        imgAI = cv2.resize(imgAI, (0,0), None, 2, 2)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (300,700))



        # insert Scaled image in Background
        # imgBG[234:654, 795:1195] = imgScaled
        imgBG[603:1353,1366:2006] = imgScaled #(640x750)
        

        # show AI Move permanently
        if stateResult:
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (300, 700))
        
        # show scores
        cv2.putText(imgBG, str(scores[0]), (785, 550), cv2.FONT_HERSHEY_PLAIN, 10, (0,0,0), 12) # AI Score
        cv2.putText(imgBG, str(scores[1]), (1895, 550), cv2.FONT_HERSHEY_PLAIN, 10, (0,0,0), 12) # Player Score

        # cv2.imshow("Image", img)
        # cv2.imshow("Image Scaled", imgScaled)
        cv2.imshow("Rock-Paper-Scissors Game", imgBG)
        
        key = cv2.waitKey(1)
        # Press S to start game
        if key == ord('s'):
            startGame = True
            initialTime = time.time()
            stateResult = False

        # Press Q to quit loop and destroy windows
        if key == ord('q'):
            quit = True
            cv2.destroyAllWindows()
            for i in range(2):
                
                cv2.waitKey(1)
            break
    if quit==True:
        break
