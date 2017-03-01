import cv2
import numpy as np
import time


#define constants and vary parameters here
#file Path
# "C:\Users\sohamBee\Desktop\Mine\"
FILEPATH = "Y:\\"

#Minimum area for filtering
MINAREA = 10


#init kernels
N = 15
kernClose = np.ones((N,N))
N = 10
kernOpen = np.ones((N,N))

#file number counter
num = 10001

#Size of images
CROPSIZE = 480
OUTSIZE = 500

# Set up the detector with default parameters.
#add filter by area param 
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = MINAREA

params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)


#####################################################################################

# binarizing images
def getRed(img):      
    lowerRed = cv2.inRange(img,(175,70,70),(180,255,255))
    upperRed = cv2.inRange(img,(0,70,70),(9,255,255))
    redImg = np.uint8( np.logical_or(lowerRed,upperRed) * 255)
 
    #close
    temp = cv2.dilate(redImg,kernClose)
    temp = cv2.erode(temp,kernClose)   
    #open
    temp = cv2.erode(temp,kernOpen)
    res = cv2.dilate(temp,kernOpen)
    
    return np.subtract(255,res)
    

def getBlue(img):
    blueImg = cv2.inRange(img,(100,150,40),(150,255,255))    
    
    #close
    temp = cv2.dilate(blueImg,kernClose)
    temp = cv2.erode(temp,kernClose)    
    #open
    temp = cv2.erode(temp,kernOpen)
    res = cv2.dilate(temp,kernOpen)
    
    #return inverted image
    return np.subtract(255,res)

def getGreen(img):
    greenImg = cv2.inRange(img,(35,150,70),(55,255,255))    #change params
    
    #close
    temp = cv2.dilate(greenImg,kernClose)
    temp = cv2.erode(temp,kernClose)   
    #open
    temp = cv2.erode(temp,kernOpen)
    res = cv2.dilate(temp,kernOpen)
    
    return np.subtract(255,res)
    
    
    
    
def getCentroids(bwImg):
    keypoints = detector.detect(bwImg)
    # sort keypoints by size
#    keypoints.sort(key = lambda x: x.size)    
    
    cents = []
    for key in keypoints:
        P = (key.pt[0],key.pt[1])
        cents.append(P)
    
    return cents

#################################################################################

def normalizePoints(points,scale):
    resPoints = []
    for pt in points:
        n0 = int(round(pt[0] * scale))        
        n1 = int(round(pt[1] * scale))
        resPoints.append((n0,n1))
    
    return resPoints



def getBlankImg(size):
    blank = np.uint8(np.ones((size,size,3)) * 255)
    return blank
    

def drawObjects(outImg, points, color = (2,254,2)):
    for P in points:
        cv2.circle(outImg,P, 18, color , thickness = -1)
    return outImg # no need to store it , failsafe
    
    
def drawBot(outImg,redPt,bluePt):
    cv2.circle(outImg,bluePt, 35, (253,3,3) , thickness = -1)
    cv2.circle(outImg,redPt, 12, (4,4,251), thickness = -1)
    


    
def sendImg(outImg, path):
    global num
    cv2.imwrite(path+"im"+str(num)+".png" , outImg)
    num += 1
#    time.sleep(0.05)


###################################################################################


def initGreen(cam):
    ret,inpImg = cam.read()
    start = (len(inpImg[0]) - CROPSIZE)/2
    rawImg = np.uint8(255 * np.ones((500,500,3)) );
    rawImg[10:490 , 10:490, :] = inpImg[:, 80 : 560, : ]
        
        
    
    #binarize images  ************************************************
    hsvImg = cv2.cvtColor(rawImg, cv2.COLOR_BGR2HSV)
    green = getGreen(hsvImg)
    
    #green circles
    greenPoints= getCentroids(green)
    return normalizePoints(greenPoints,OUTSIZE/float(CROPSIZE))
    


def startGame():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    print "READY!"
    #setting default values in case of error
    redPoint = (0,0)
    bluePoint = (255,255)


    greenPoints = initGreen(cam)
    
    raw_input("Press Enter to START");
    
    startTime = time.clock()
    
    while cam.isOpened():
        
        
        
        #capture image and crop it
        ret,inputImg = cam.read()

        rawImg = np.uint8(255 * np.ones((500,500,3)) );
        

        rawImg[10:490 , 10:490, :] = inputImg[:, 80 : 560, : ]
        
        
        cv2.imshow("INPUT", rawImg)
        
        #binarize images  ************************************************
        hsvImg = cv2.cvtColor(rawImg, cv2.COLOR_BGR2HSV)
        red = getBlue(hsvImg)
        blue = getRed(hsvImg)
      
      
        #new blank image
        output = getBlankImg(OUTSIZE)
        
        #green circles
        drawObjects(output, greenPoints)
        
        #draw bot
        redPoints = normalizePoints(getCentroids(red),OUTSIZE/float(CROPSIZE))
        if len(redPoints) ==0:
            print "red"
            
        else:
            redPoint = redPoints[0]
        bluePoints = normalizePoints(getCentroids(blue),OUTSIZE/float(CROPSIZE))
        if len(bluePoints) ==0:
            print "blue"
            
        else:
            bluePoint = bluePoints[0]
        
        drawBot(output,redPoint,bluePoint)
        
        #send image and display it
        sendImg(output,FILEPATH)
        cv2.imshow("ARENA", output)
        
        #exit if Escape key pressed
        k = cv2.waitKey(5)
        if k == 27:
            break;
    
    #endGame
    cam.release()
    cv2.destroyAllWindows()
    
    finalTime = time.clock()
    return round(finalTime - startTime , 3)



########################################################################################################


print startGame(),
print "seconds"
