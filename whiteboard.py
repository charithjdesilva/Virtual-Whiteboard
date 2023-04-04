import cv2
import numpy as np
import keyboard

vidCap = cv2.VideoCapture(0)
vidCap.set(3, 1366)   # set width to 1366px, id number of width is 3
vidCap.set(4, 768)   # set height to 768px, id number of height is 4
vidCap.set(10, 150) #change brightness to 150

myColors = [#[0,154,130,160,255,255],     # orange pen color, -----------change
            [9, 129, 96, 32, 255, 255],    # yellow highlighter, -----------change
            [101, 105, 64, 133, 255, 139]    # blue markerpen
            ]   # min and max HSV values

myColorValues = [#[53,153,255],    # colors drawn on the screen referencing my color ranges
                 [0,204,255],
                 [153,51,0]]

myPoints = []         # [x, y, colorId, penSize]

# color detection
def findColor(img, myColors, myColorValues, penSize):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgResizeHSV = cv2.resize(imgHSV, (1366//4, 768//4))
    count = 0
    newPoints = []    # creates an empty list for every point

    # detect all the colors in the list
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        maskResize = cv2.inRange(imgResizeHSV, lower, upper)
        x,y = getContours(mask)
        xx,yy = getContours(maskResize)
        cv2.circle(imgBlank, (x,y), penSize, myColorValues[count], cv2.FILLED)    # draw a circle on the image
        cv2.circle(imgResize, (xx,yy), 10, myColorValues[count], cv2.FILLED)    # draw a circle on the image
        if x != 0 and y !=0 and draw == True:     # if x,y values are not 0,0 append the point
            newPoints.append([x, y, count, penSize])
        count += 1
        # cv2.imshow(str(color), mask)
    return newPoints

# function to get contours of an image
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # find contours of an image  (RETR_EXTERNEL is used to find outer corners)

    x, y, width, height = 0,0,0,0   # to return if area of contour > 500 not detected

    # loop through each contour
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)

        # give minimum width for the area, so that it does not detect any noise
        if area > 200:
            # draw contours to see them clearly
            # cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)  # contours will be drawn in the image provided
            
            # curve length helps to approximate the corners of the shapes
            peri = cv2.arcLength(cnt, True) #length of the each contour, True means closed
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)    # approximate how many corner points, , True means shape is closed

            # create a bounding box araound the detected object
            x, y, width, height = cv2.boundingRect(approx)
    return x + width//2, y      # return the top, center point of the bounding box

# draw on the each point in myPoints list
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgBlank, (point[0],point[1]), point[3], myColorValues[point[2]], cv2.FILLED)    # draw a circle on the image

# pen size
penSize = 8
def penSizeChanger(penSize, minn=1, maxn=15):
    if penSize < minn:
        return minn
    elif penSize > maxn:
        return maxn
    else:
        return penSize

draw = False    # used for enable and disable pen
clear = False

while True:
    success, img = vidCap.read()
    imgResult = cv2.flip(img.copy(),1)
    imgBlank = np.full_like(img, 255)   # create a blank image like the image

    if clear == True:
        cv2.rectangle(imgBlank, (0, 0), (imgBlank.shape[1],imgBlank.shape[0]), (255, 255, 255), cv2.FILLED)
        clear = False
        myPoints = []
        cv2.imshow("wb", imgBlank)
        cv2.waitKey(1)

    imgResize = cv2.resize(cv2.flip(img.copy(),1), (1366//4, 768//4))   # parameters image, width, height

    # when we find a color send it to drawOnCanvas function
    newPoints = findColor(cv2.flip(img.copy(),1), myColors, myColorValues, penSize)
    if len(newPoints) != 0:        # if returned newPoints list is not empty
        for newPoint in newPoints:      # for loop is used we may receive multiple points for multiple pen
            myPoints.append(newPoint)
    
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.namedWindow("wb", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("wb",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    cv2.namedWindow("Webcam")
    cv2.moveWindow("Webcam", 0,0)

    cv2.imshow("wb", imgBlank)
    cv2.imshow("Webcam", imgResize)

    # if keyboard.is_pressed("e"):
    #     imgBlank = np.zeros_like(img)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord('q'):
        break
    elif pressedKey == ord('w'):
        if draw == True:
            draw = False
        elif draw == False:
            draw = True
    elif pressedKey == ord('e'):
        clear = True
    elif pressedKey == ord(','):
        penSize = penSizeChanger(penSize-1)
    elif pressedKey == ord('.'):
        penSize = penSizeChanger(penSize+1)
        
        

