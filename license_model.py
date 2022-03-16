import cv2
import imutils
import pytesseract
from scipy.__config__ import show

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

class LicenseDetector():
    def to_grayscale(self, im):
        im_grayscale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return cv2.bilateralFilter(im_grayscale, 11, 17, 17)

    def find_edges(self, im):
        return cv2.Canny(im, 30, 200)

    def find_contours(self, im):
        contour, n = cv2.findContours(im.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contour

    def detect(self, path, show_steps = False):
        im = cv2.imread(path)
        im = imutils.resize(im, width = 500)
        if show_steps:
            cv2.imshow("original image", im)
            cv2.waitKey(0)

        im_grayscale = self.to_grayscale(im)
        if show_steps:
            cv2.imshow("grayscale image", im_grayscale)
            cv2.waitKey(0)

        edges = self.find_edges(im_grayscale)
        if show_steps:
            cv2.imshow("Edges", edges)
            cv2.waitKey(0)
        
        contour = self.find_contours(edges)
        if show_steps:
            temp = im.copy()
            cv2.drawContours(temp, contour, -1, (0,255,0), 3)
            cv2.imshow("Contours", temp)
            cv2.waitKey(0)

        contour = sorted(contour, key = cv2.contourArea, reverse=True)[:30]
        scrCount = None
        if show_steps:
            temp = im.copy()
            cv2.drawContours(temp, contour, -1, (0,255,0), 3)
            cv2.imshow("Top Contours", temp)
            cv2.waitKey(0)

        for c in contour:
            p = cv2.arcLength(c, True)
            est = cv2.approxPolyDP(c, 0.018*p, True)
            if len(est) == 4:
                scrCount = est
                x,y,w,h = cv2.boundingRect(c)
                new_im = im[y:y+h,x:x+w]
                #cv2.imwrite('./'+path+'_bounding_box.png', new_im)
                break
        
        if show_steps:
            cv2.drawContours(im, [scrCount], -1, (0,255,0), 3)
            cv2.imshow('liscense plate bounding box', im)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return new_im

#lm = LicenseDetector()
#lm.detect('test.jpg', True)


