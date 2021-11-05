import cv2
import math
import imutils
import numpy as np
import warnings
from sklearn.cluster import KMeans
from skimage.morphology import *
from skimage.util import *

class OD_CV:

    def loadImage(self, filepath):
        return cv2.imread(filepath)

    def resizeImage(self, image, kar, width, height):
        if kar:
            return imutils.resize(image, width=width)
        else:
            return cv2.resize(image, (width, height))

    def maskIMG(self, image, pts):
        mask = np.zeros(image.shape[:2], np.uint8)
        mask = cv2.drawContours(mask, [pts], -1, (255,255,255), -1)
        image = cv2.bitwise_and(image.copy(), image.copy(), mask=mask)
        return image

    def cropIMG(self, image, coords):
        return image[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]

    def dmntCOLOR(self, image):
        image = cv2.resize(image, (0, 0), None, 0.5, 0.5)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            clt = KMeans(n_clusters=5, random_state=0).fit(image.reshape(-1, 3))
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        hist, _ = np.histogram(clt.labels_, bins=numLabels)
        # normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()
        palette = np.zeros((40, 200, 3), dtype="uint8")
        startX = 0
        # loop over the percentage of each cluster and the color of
        # each cluster
        for percent, color in zip(hist, clt.cluster_centers_):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 200)
            cv2.rectangle(palette, (int(startX), 0), (int(endX), 40), color.astype("uint8").tolist(), -1)
            startX = endX
        return palette

    def thinning(self, image, flag):
        image = img_as_float(image)
        if flag:    #live streaming, faster computation
            skeleton = skeletonize(image > 0)
        else:   # upload image mode
            skeleton = skeletonize(image > 0, method='lee')
        return img_as_ubyte(skeleton)

    def thresholding(self, image, auto, lower, max):
        if auto:
            _, image = cv2.threshold(image.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        else:
            _, image = cv2.threshold(image.copy(), lower, max, cv2.THRESH_BINARY)
        return image

    def color_CVT(self, image, flag):
        if flag==1:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif flag==2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    def compareIMG(self, image):
        h,w = image[0].shape[:2]
        bg = np.zeros((h*2+3, w*2+3, 3), np.uint8)
        bg[0:h, 0:w] = image[0]
        bg[0:h, w+3:w*2+3] = image[1]
        bg[h+3:h*2+3, 0:w] = image[2]
        bg[h+3:h*2+3, w+3:w*2+3] = image[3]
        bg[0:h*2+3, w:w+3] = (255,255,255)
        bg[0:h * 2 + 3, w+1:w + 2] = (0,0,0)
        bg[h:h+3, 0:w*2+3] = (255,255,255)
        bg[h+1:h + 2, 0:w * 2 + 3] = (0,0,0)
        return bg

    def Color_picker(self, color, size, wid=(10,20)):
        image = np.zeros((size[0], size[1], 3), np.uint8)
        image[:] = color
        if wid[0]>0:
            cv2.rectangle(image, (int(size[0]*.01), int(size[1]*.01)), (int(size[0]*.99), int(size[1]*.99)), (0,0,0), wid[0], cv2.LINE_AA)
        if wid[1]>0:
            cv2.rectangle(image, (int(size[0]*.1), int(size[1]*.1)), (int(size[0]*.9), int(size[1]*.9)), (255,255,255), wid[1], cv2.LINE_AA)
        return image

    def drawPrimitives(self, image, flag, points, color, thick, width=None, height=None):
        if flag==1:
            cv2.polylines(image, points, True, color, thick)
        elif flag==2:
            cv2.rectangle(image, (points[0]-10, points[1]-10), (points[0]+points[2]+10, points[1]+points[3]+10), color, thick)
        elif flag==3:
            x, y, w, h = points
            width_Total = x+int(w*0.05)+width
            if width_Total>x+w+10:
                width_Total = x+w+10
            cv2.rectangle(image, (x+int(w*0.05),y-10-height), (width_Total, y-10-2), color, thick)
        elif flag == 4:
            x, y, w, h = points
            if width!=0:
                w = width
            cv2.rectangle(image, (x-10,y+10+h), (x+10+w, y+10+h+height), color, thick)

    def drawText(self, flag, image, text, coords, fontstyle, color, thick, height=None):
        font = None
        if fontstyle == 0:
            font = cv2.FONT_HERSHEY_COMPLEX
        elif fontstyle == 1:
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        elif fontstyle == 2:
            font = cv2.FONT_HERSHEY_DUPLEX
        elif fontstyle == 3:
            font = cv2.FONT_HERSHEY_PLAIN
        elif fontstyle == 4:
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        elif fontstyle == 5:
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        elif fontstyle == 6:
            font = cv2.FONT_HERSHEY_TRIPLEX
        elif fontstyle == 7:
            font = cv2.FONT_ITALIC
        x, y, w, h = coords
        if flag==1:
            cv2.putText(image, text, (x+int(w*0.07),y-19), font, thick, color, 1)
        elif flag==2:
            cv2.putText(image, text, (x-10,y+10+h+height-5), font, thick, color, 1)

    def canny(self, image, GK_size, GSigma, DK_size, D_i, EK_size, E_i, cAuto, cThres_L, cThres_H, isDIL, isERO, isThin=None):
        imgGray = self.color_CVT(image.copy(), 1)
        image = cv2.GaussianBlur(imgGray, (GK_size, GK_size), GSigma)
        if cAuto:
            sigma = 0.33
            v = np.median(image.copy())
            # apply automatic Canny edge detection using the computed median
            lower = int(max(0, (1.0 - sigma) * v))
            upper = int(min(255, (1.0 + sigma) * v))
        else:
            lower, upper = cThres_L, cThres_H
        image = cv2.Canny(image, lower, upper)
        if isThin:
            image = self.thinning(image)
        edge = image.copy()
        if isDIL:
            Dial_K = np.ones((DK_size, DK_size))
            image = cv2.dilate(image, Dial_K, iterations=D_i)
        if isERO:
            Ero_K = np.ones((EK_size, EK_size))
            image = cv2.erode(image, Ero_K, iterations=E_i)
        return image, edge

    def sobel(self, image, GK_size, GSigma, DK_size, D_i, EK_size, E_i, Ksize, isDIL, isERO, isThin, Thres_auto, Thres_L, Thres_H, isThres, live_flag):
        imgGray = self.color_CVT(image.copy(), 1)
        imgBlur = cv2.GaussianBlur(imgGray, (GK_size, GK_size), GSigma)
        Sobel_X = cv2.Sobel(imgBlur.copy(), cv2.CV_64F, 1, 0, ksize=Ksize)
        Sobel_Y = cv2.Sobel(imgBlur.copy(), cv2.CV_64F, 0, 1, ksize=Ksize)
        sobel_img = cv2.bitwise_or(cv2.convertScaleAbs(Sobel_X), cv2.convertScaleAbs(Sobel_Y))
        if isThres:
            sobel_img = self.thresholding(sobel_img.copy(), Thres_auto, Thres_L, Thres_H)
        if isThin:
            sobel_img = self.thinning(sobel_img, live_flag)
        image = sobel_img
        edge = image.copy()
        if isDIL:
            Dial_K = np.ones((DK_size, DK_size))
            image = cv2.dilate(image, Dial_K, iterations=D_i)
        if isERO:
            Ero_K = np.ones((EK_size, EK_size))
            image = cv2.erode(image, Ero_K, iterations=E_i)
        return image, edge

    def prewitt(self, image, GK_size, GSigma, DK_size, D_i, EK_size, E_i, isDIL, isERO, isThin, Thres_auto, Thres_L, Thres_H, isThres, live_flag):
        imgGray = self.color_CVT(image.copy(), 1)
        imgBlur = cv2.GaussianBlur(imgGray, (GK_size, GK_size), GSigma)
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernelx2 = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernely2 = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        kernels = [kernelx, kernelx2, kernely, kernely2]
        prewitt_img = np.zeros_like(imgGray)
        for k in kernels:
            prewitt_img = cv2.bitwise_or(prewitt_img, cv2.filter2D(imgBlur.copy(), -1, k))
        if isThres:
            prewitt_img = self.thresholding(prewitt_img.copy(), Thres_auto, Thres_L, Thres_H)
        if isThin:
            prewitt_img = self.thinning(prewitt_img, live_flag)
        image = prewitt_img
        edge = image.copy()
        if isDIL:
            Dial_K = np.ones((DK_size, DK_size))
            image = cv2.dilate(image, Dial_K, iterations=D_i)
        if isERO:
            Ero_K = np.ones((EK_size, EK_size))
            image = cv2.erode(image, Ero_K, iterations=E_i)
        return image, edge

    def getTarget_Contour(self, image, image_edg, minArea, shapes, circular, color, thick):
        contours, _ = cv2.findContours(image_edg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        finalCountours = []
        for c in contours:
            for i, shape in enumerate(shapes):
                if not shape:
                    continue
                area = cv2.contourArea(c)
                if area > minArea[i]:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    bbox = cv2.boundingRect(approx)
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    rbox = np.int0(box)
                    if i==0 and len(approx) == 3:    #Shape >>> vertices

                        finalCountours.append((approx, bbox, c, i, rbox))
                    elif i==1 and len(approx) == 4:
                        finalCountours.append((approx, bbox, c, i, rbox))
                    elif i==2:
                        if len(approx) < 8:
                            continue
                        circularity = 4 * math.pi * (area / (peri*peri))
                        if circular[0] < circularity < circular[1]:
                            finalCountours.append((approx, bbox, c, i, rbox))
                    elif i==3:
                        finalCountours.append((approx, bbox, c, i, rbox))
        finalCountours = sorted(finalCountours, key=lambda x:x[1], reverse=True)
        if thick==0:
            thick = -1
        for cont in finalCountours:
            cv2.drawContours(image, [cont[2]], -1, color, thick)
        return finalCountours, image

    def reorder(self, points):
        NewPoints = np.zeros_like(points)
        points = points.reshape((4,2))
        add = points.sum(1)
        NewPoints[0] = points[np.argmin(add)]
        NewPoints[2] = points[np.argmax(add)]
        d_dx = np.diff(points, axis=1)
        NewPoints[1] = points[np.argmin(d_dx)]
        NewPoints[3] = points[np.argmax(d_dx)]
        return NewPoints

    def warpImg(self, image, points, size, pad=3):
        points = self.reorder(points)
        # if not size:
        w, h = points[1][0][0] - points[0][0][0], points[3][0][1]-points[0][0][1]
        sw,sh = w/size[0], h/size[1]
        # w,h = size
        pts1 = np.float32(points)
        pts2 = np.float32([[0,0], [w,0], [w,h], [0,h]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(image, matrix, (w,h))

        imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]   #remove boundary
        return imgWarp, (sw,sh)

    def findDist(self, flag, pts, scale, unit, deci):
        unit_conv = 1
        if unit[0]==0:
            unit_conv = 1
        elif unit[0]==1:
            unit_conv = 10
        elif unit[0]==2:
            unit_conv = 1000
        if unit[1]==0:
            unit_conv /= 1
        elif unit[1]==1:
            unit_conv /= 10
        elif unit[1]==2:
            unit_conv /= 1000

        def dist(pt1, pt2):
            return ((pt2[0] // scale[0] - pt1[0] // scale[0]) ** 2 + (pt2[1] // scale[1] - pt1[1] // scale[1]) ** 2) ** 0.5
        # if flag==1:     # rect
        pts = self.reorder(pts)
        if flag==1:     #rect
            p1, p2, p3 = pts[0][0], pts[1][0], pts[3][0]
        else:
            p1, p2, p3 = pts[0], pts[1], pts[3]
        if p1[1]==p2[1]:
            newW = (p2[0]-p1[0])//scale[0]
        else:
            newW = dist(p1, p2)
        if p1[0]==p3[0]:
            newH = (p3[1]-p1[1])//scale[1]
        else:
            newH = dist(p1, p3)

        newW = newW*unit_conv
        newH = newH*unit_conv
        return "{:.{}f}".format(newW, deci), "{:.{}f}".format(newH, deci)

    def deviceList(self):
        index = 0
        arr, res = [], []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(str(index))
                res.append((cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            cap.release()
            index += 1
        return arr, res