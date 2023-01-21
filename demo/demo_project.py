from twilio.rest import Client

import cv2
import os
import time
import handTrackingModule as htm
from mediapipe.python._framework_bindings import packet
# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client()
# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+6288223384848'

global history
history = []
def sendWa(msg):
    if msg == 0:
        history.clear()
        return 0
    elif not msg in history:
        history.append(msg)
        client.messages.create(body=msg,
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)
    print(history)

def getNumber(ar):
    s=""
    for i in ar:
       s+=str(ar[i]);
       
    if(s=="00000"):
        sendWa(0)        
        return (0)
    elif(s=="01000"):
        sendWa("led1 on")
        return(1)
    elif(s=="01100"):
        sendWa("led2 on")
        return(2) 
    elif(s=="01110"):
        sendWa("led3 on")
        return(3)
    elif(s=="01111"):
        sendWa("t1 4 jari")
        return(4)
    elif(s=="11111"):
        sendWa("all off")
        return(5) 
    elif(s=="01001"):
        return(6)
    elif(s=="01011"):
        return(7)      
 
wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=0.75)
while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    tipId=[4,8,12,16,20]
    if(len(lmList)!=0):
        fingers=[]
        #thumb
        if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                fingers.append(1)
        else :
                fingers.append(0)
        #4 fingers
        for id in range(1,len(tipId)):
            
            if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                fingers.append(1)
            
            else :
                fingers.append(0)
        
           
        cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)   
        cv2.putText(img,str(getNumber(fingers)),(45,375),cv2.FONT_HERSHEY_PLAIN,
                                     10,(255,0,0),20)  
        
     
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
    cv2.imshow("image",img)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break
