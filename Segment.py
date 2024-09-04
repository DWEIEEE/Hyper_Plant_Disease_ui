import numpy as np
import cv2 as cv
import os
import scipy.io
from scipy.ndimage import zoom

class Segmentation:
    def __init__(self, leaf_size, threshold, img_size):
        self.leaf_size = leaf_size
        self.threshold = threshold
        self.img_size = img_size

    def normalization(self,img):
        min_value = np.min(img)
        max_value = np.max(img)
        normalized_img = (img - min_value) / (max_value - min_value)
        normalized_img = cv.convertScaleAbs(normalized_img, alpha=255)
        return normalized_img

    def process(self, img):
        self.img = img
        #print(f"img shape : {img.shape}")
        self.band = img.shape[2]
        self.limit_area = img.shape[0] * img.shape[1]
        self.stored_img = np.zeros_like(img[:,:,0])
        for band in range(self.band-2):
            self.stored_img = self.stored_img + img[:,:,band+1]

        self.normal_img = self.normalization(self.stored_img)
        _, thresh = cv.threshold(self.normal_img,40,255,cv.THRESH_BINARY)
        self.contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_SIMPLE)
        self.area_list = []
        for index,contour in enumerate(self.contours):
            x, y, w, h = cv.boundingRect(contour)
            area = int(cv.contourArea(contour))
            if (w*h) >= self.leaf_size and (w*h) < self.limit_area: # limit of area
                self.area_list.append([index, x, y, w, h, area])
                #print(f"idx : {index}, w : {w}, h : {h} size : {area} ({w*h})  / {self.img_size*self.img_size}")
        self.stack_image_list = self.generate()
        return self.area_list, self.stack_image_list

    def generate(self):
        stack_image_list = np.empty((0, 224, 224, 24), dtype=np.float64)
        for idx, (index, x, y, w, h, area) in enumerate(self.area_list):
            filled_img = np.zeros_like(self.normal_img)
            cv.drawContours(filled_img, self.contours, index, (255), thickness=cv.FILLED)
            _, binary_img = cv.threshold(filled_img,127, 1, cv.THRESH_BINARY)
            binary_img = binary_img.astype(np.float64)
            output_img = np.zeros((224, 224, 24), dtype=np.float64)
            for band in range(self.band):
                background = np.zeros((224, 224), dtype=np.float64)
                tmp_img = self.img[:,:,band] * binary_img
                tmp_img = tmp_img[y:(y+h),x:(x+w)]
                bw = background.shape[1]
                bh = background.shape[0]
                if (w <= (self.img_size//2)) and (h <= (self.img_size//2)):
                    #print(f"h: {h}, w: {w}")
                    scale = min((self.img_size//w),(self.img_size//h))
                    tmp_img = zoom(tmp_img, scale//2)
                    a_h = tmp_img.shape[0]
                    a_w = tmp_img.shape[1]
                    #print(f"scale : {scale}, h: {a_h}, w: {a_w}")
                else:
                    a_h = h
                    a_w = w
                try:
                    background[((bh-a_h)//2):(((bh-a_h)//2)+a_h),((bw-a_w)//2):(((bw-a_w)//2)+a_w)] = tmp_img
                except:
                    try:
                        tmp_img_resized = zoom(tmp_img, 0.5)
                        t_h = tmp_img_resized.shape[0]
                        t_w = tmp_img_resized.shape[1]
                        background[((bh-t_h)//2):(((bh-t_h)//2)+t_h),((bw-t_w)//2):(((bw-t_w)//2)+t_w)] = tmp_img_resized
                    except:
                        print("Still not fixed")
                output_img[:,:,band] = background
            stack_image_list = np.append(stack_image_list, [output_img], axis=0)
            #print(f"iii stack_image_list: {stack_image_list.shape}")
        return stack_image_list

