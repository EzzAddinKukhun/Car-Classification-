
import cv2
import numpy as np

class Shape:

    def __init__(self,name,ident,a0,a1, b0,b1,c0,c1,d0,d1,shapeborder,pointer,done):
        self.name = name
        self.ident = ident
        self.a0 = a0
        self.a1 = a1
        self.b0 = b0
        self.b1 = b1
        self.c0 = c0
        self.c1 = c1
        self.d0 = d0
        self.d1 = d1
        self.done = done
        self.shapeborder = shapeborder
        self.pointer = pointer

def searchArray (element,array):
    flag = 1
    for i in range(len(array)):
        if (element.ident == array[i].ident):
            flag = 0
            break
    return flag

def setVisisted (element,LargeArray):
   for i in range(len(LargeArray)):
       if element.ident == LargeArray[i].ident:
           LargeArray[i].done = True

# def checkIfElementIsExist (currshape,car_parts):
#     addresult = searchArray(currshape, car_parts)
#     if (addresult == 1):
#         car_parts.append(currshape)

def updateCarParts (nextshape,currshape,car_parts):
    search_about_next_shape = searchArray(nextshape, car_parts)
    search_about_current_shape = searchArray(currshape, car_parts)

    if (search_about_next_shape == 1):
        car_parts.append(nextshape)
    if (search_about_current_shape == 1):
        car_parts.append(currshape)

def connectCircleWithRectangle (nextshape,currshape):
    if (abs(nextshape.d1-currshape.a1) <=20 or abs(nextshape.c1-currshape.a1) <=20)\
      and (abs(nextshape.d0-currshape.a0) <=150 or abs(nextshape.c0-currshape.a0) <=150):
        currshape.pointer = nextshape
        return  True
    else :
        return  False

def connectRectangleWithCircle (nextshape,currshape):
    if (abs(nextshape.a1-currshape.d1) <=20 or abs(nextshape.a1-currshape.c1) <=20)\
      and (abs(nextshape.a0-currshape.d0) <=150 or abs(nextshape.a0-currshape.c0) <=150):
        return  True
    else:
        return False

def connectRectangleToRectangle (nextshape,currshape,arc):
    if (abs(nextshape.b1 - currshape.c1) <= 20 and abs(nextshape.b0 - currshape.c0) < 0.5 * arc)\
        or (abs(nextshape.c1 - currshape.b1) <= 20 and abs(nextshape.c0 - currshape.b0) < 0.5 * arc):
        nextshape.pointer = currshape
        currshape.pointer = nextshape
        return True
    else:
        return False



def printDebug (car_parts):
    for i in range(len(car_parts)):
        print("*****END****" + car_parts[i].name + "*********")
        print("ID OF ELEMENT" + str(car_parts[i].ident))
        print("TOP COORDINATE" + "[" + str(car_parts[i].x0) + "," + str(car_parts[i].y0) + "]")
        print("DOWN COORDINATE" + "[" + str(car_parts[i].x1) + "," + str(car_parts[i].y1) + "]")



img = cv2.imread("test.png")
grayimg = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(grayimg,127,255,cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)


# create array of shapes to save data about each shape
shapes = []
car_parts = []
identification = 0

for contour in contours:
    shapeborder = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True), True)
    x  = shapeborder.ravel()[0]
    y = shapeborder.ravel()[1]
    cv2.drawContours(img, [shapeborder], -1, (255, 255, 255), cv2.FILLED)
    cv2.drawContours(img,[shapeborder], 0, (0,0,0), 2)

    if (len(shapeborder) == 3):
         shape = Shape("TRIANGLE",identification,shapeborder.ravel()[0],shapeborder.ravel()[1],shapeborder.ravel()[2],
                       shapeborder.ravel()[3],shapeborder.ravel()[4],shapeborder.ravel()[5],-1,-1,shapeborder,None,False)
         shapes.append(shape)

         # cv2.putText(img,"TRIANGLE", (x,y), cv2.FONT_ITALIC, 0.5,(255,0,0))
         identification = identification + 1


    elif (len(shapeborder) == 4):
        x,y,w,h = cv2.boundingRect(shapeborder)
        ratio = float(w)/h;
        if (ratio == 1):
         shape = Shape("SQUARE",identification, shapeborder.ravel()[0], shapeborder.ravel()[1], shapeborder.ravel()[2], shapeborder.ravel()[3],
                       shapeborder.ravel()[4], shapeborder.ravel()[5], shapeborder.ravel()[6], shapeborder.ravel()[7],shapeborder,None,False)
         shapes.append(shape)
         # cv2.putText(img, "SQUARE" , (x, y), cv2.FONT_ITALIC, 0.5, (0, 0, 0))
         identification = identification + 1

        else:
         if not(shapeborder.ravel()[0]==0 and shapeborder.ravel()[1]==0):
             shape = Shape("RECTANGLE",identification, shapeborder.ravel()[0], shapeborder.ravel()[1], shapeborder.ravel()[2], shapeborder.ravel()[3],
                       shapeborder.ravel()[4], shapeborder.ravel()[5], shapeborder.ravel()[6], shapeborder.ravel()[7],shapeborder,None,False)
             shapes.append(shape)
             # cv2.putText(img,"RECTANGLE", (x, y), cv2.FONT_ITALIC, 0.5, (0, 0, 0))
             identification = identification + 1


    else:
        shape = Shape("CIRCLE",identification, shapeborder.ravel()[0],shapeborder.ravel()[1], -1,  -1,-1,-1,-1,-1,shapeborder,None,False)
        shapes.append(shape)
        # cv2.putText(img, "CIRCLE", (x, y), cv2.FONT_ITALIC, 0.5, (0, 0, 0))
        identification = identification + 1



cc = len(shapes)
x=0


for i in range(0,cc):
    currshape = shapes.__getitem__(i)
    namecurr = currshape.name

    for x in range (0,cc):
         if namecurr == "RECTANGLE":
            nextshape = shapes.__getitem__(x)

            if (nextshape.name == "TRIANGLE" and abs(nextshape.a0 - currshape.a0)<=20) and abs(nextshape.a1-currshape.a1)<=20  and nextshape.ident != currshape.ident:
                updateCarParts(nextshape, currshape, car_parts)

            elif nextshape.name == "CIRCLE" and connectRectangleWithCircle (nextshape,currshape) and nextshape.ident != currshape.ident:
                updateCarParts(nextshape, currshape, car_parts)

            elif nextshape.name == "TRIANGLE" and abs(nextshape.c0-currshape.a0) <=20 and abs(nextshape.c1-currshape.a1)<=20 and nextshape.ident != currshape.ident:
                updateCarParts(nextshape, currshape, car_parts)

            elif nextshape.name == "RECTANGLE":
                 x1, y1, w1, h1 = cv2.boundingRect(nextshape.shapeborder)
                 x2, y2, w2, h2 = cv2.boundingRect(currshape.shapeborder)
                 arc = w2 if w2 > w1 else w1
                 if connectRectangleToRectangle (nextshape,currshape,arc):
                    updateCarParts(nextshape, currshape, car_parts)


         elif namecurr == "CIRCLE":
            nextshape = shapes.__getitem__(x)
            if nextshape.name == "RECTANGLE" and connectCircleWithRectangle (nextshape,currshape) and nextshape.ident != currshape.ident :
             updateCarParts (nextshape,currshape,car_parts)


         elif namecurr == "TRIANGLE":

            if   nextshape == "RECTANGLE" and abs(nextshape.a0 - currshape.a0)<=20 and abs(nextshape.a1-currshape.a1)<=20 and nextshape.ident != currshape.ident:
                updateCarParts(nextshape, currshape, car_parts)

            elif nextshape=="RECTANGLE" and abs(nextshape.a0-currshape.c0)<=20  and abs(nextshape.a1-currshape.c1)<=20 and nextshape.ident != currshape.ident:
                updateCarParts(nextshape, currshape, car_parts)



for i in range(len(car_parts)):
    currshape = car_parts[i]
    print(currshape.name=="TRIANGLE")
    if (currshape.name == "TRIANGLE"):
        for x in range (len(car_parts)):
          top_rectangle = car_parts[x]
          if top_rectangle.name == "RECTANGLE" and abs(top_rectangle.a0 - currshape.a0) <= 20 and abs(top_rectangle.a1 - currshape.a1) <= 20:
              print(top_rectangle.pointer.name)
              mid_rectangle = top_rectangle.pointer
              print(mid_rectangle.name)
              x1, y1, w1, h1 = cv2.boundingRect(top_rectangle.shapeborder)
              x2, y2, w2, h2 = cv2.boundingRect(mid_rectangle.shapeborder)
              arc = w2 if w2 > w1 else w1

              print(h1)
              print(h2)
              if (h1 > h2):
                cv2.putText(img, "CAR", (currshape.a0-100, currshape.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                cv2.putText(img, "CLASS1", (top_rectangle.a0, top_rectangle.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                car_parts[x].done = True
                car_parts[i].done = True
                mid_rectangle.done = True
                break

              elif (h1 < h2) and (abs(mid_rectangle.b1 - top_rectangle.c1) <= 10 and abs(mid_rectangle.b0 - top_rectangle.c0) <=10) :
                  cv2.putText(img, "CAR", (currshape.a0-100, currshape.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                  cv2.putText(img, "CLASS3", (top_rectangle.a0, top_rectangle.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                  car_parts[x].done = True
                  car_parts[i].done = True
                  mid_rectangle.done = True

                  break

              else:
                  cv2.putText(img, "CAR", (currshape.a0-100, currshape.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                  cv2.putText(img, "CLASS2", (top_rectangle.a0, top_rectangle.a1), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0))
                  car_parts[x].done = True
                  car_parts[i].done = True
                  mid_rectangle.done = True

                  break




for i in range (len(shapes)):
    if shapes[i].done == False:
        if (shapes[i].name == "TRIANGLE"):
            x = shapes[i].shapeborder.ravel()[2]
            y = shapes[i].shapeborder.ravel()[3]
            cv2.putText(img, shapes[i].name, (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 0))

        elif shapes[i].name == "CIRCLE" and shapes[i].pointer != None:
            if shapes[i].pointer.name == "RECTANGLE":
             print("HHH")

        else:
         x = shapes[i].shapeborder.ravel()[0]
         y = shapes[i].shapeborder.ravel()[1]
         shape_name = None
         cv2.putText(img,shapes[i].name, (x,y), cv2.FONT_HERSHEY_TRIPLEX, 0.8,(0,0,0))



cv2.imshow("IMG",img)
cv2.waitKey(0)



