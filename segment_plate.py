import cv2
import os
import imutils
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np
from license_model import LicenseDetector
from os import listdir
from keras.preprocessing.image import load_img, img_to_array

class PlateSegmenter():
    def segment(self, im, show_steps = False):
        #im = cv2.imread(path)
        im = imutils.resize(im, width = 300)
        if show_steps:
            cv2.imshow("Original", im)
            cv2.waitKey(0)

        im_grayscale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if show_steps:
            cv2.imshow("GrayScale", im_grayscale)
            cv2.waitKey(0)

        im_blur = cv2.GaussianBlur(im_grayscale,(7,7),0)
        if show_steps:
            cv2.imshow("Blurred", im_blur)
            cv2.waitKey(0)

        im_binary = cv2.threshold(im_blur, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]              
        im_binary = cv2.bitwise_not(im_binary)
        if show_steps:
            cv2.imshow("Binary", im_binary)
            cv2.waitKey(0)

        contours, n = cv2.findContours(im_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = lambda k: cv2.boundingRect(k)[0], reverse=False)

        character_ims= []
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = h/w
            if 1<=ratio<=5:
                if h/im.shape[0]>=0.5: 
                    curr_num = im_binary[y:y+h,x:x+w]
                    curr_num = cv2.resize(curr_num, dsize=(60, 60))
                    curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                    character_ims.append(curr_num)


        if show_steps:
            fig = plt.figure(figsize=(14,4))
            grid = gs.GridSpec(ncols=len(character_ims),nrows=1,figure=fig)

            for i in range(len(character_ims)):
                fig.add_subplot(grid[i])
                plt.axis(False)
                plt.imshow(character_ims[i],cmap="gray")

            print(character_ims[0].shape)
            print(type(character_ims[0]))
            plt.show()
        

        for i in range(len(character_ims)):
            character_ims[i] = cv2.cvtColor(character_ims[i], cv2.COLOR_GRAY2RGB)
            character_ims[i] = np.expand_dims(character_ims[i], axis = 0)

        return character_ims


labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
model = tf.keras.models.load_model('trained_character_model')
lm = LicenseDetector()
ps = PlateSegmenter()
# plate = lm.detect('test.jpg')
# print("Plate", plate)

# characters = ps.segment(plate)
# for char in characters:
#     pred = model.predict(char)
#     idx = np.argmax(pred)
#     print(labels[idx])

with open('FinalProjectLabels.txt') as f:
    lines = f.readlines()
model_output = []
y_test = []

i = 0 
for file in listdir('data'):
    path = os.path.join('data', file)
    if lines[i] != 'No':
        y_test.append(lines[i])
        try:
            plate = lm.detect(path)
            characters = ps.segment(plate)
        except:
            characters = ""
        output = ""
        for char in characters:
            pred = model.predict(char)
            idx = np.argmax(pred)
            output += labels[idx]
        model_output.append(output)
    i += 1

print(model_output[0])
print(model_output[1])
print("Length of test set: ", len(y_test))
complete_correct = 0
chars_correct = 0
total_chars = 0

for i, output in enumerate(model_output):
    true_val = y_test[i]
    total_chars += len(true_val)
    
    if output == true_val:
        complete_correct += 1
        chars_correct += len(output)
    else:
        for j, c in enumerate(output):
            if j < len(true_val) and c == true_val[j]:
                chars_correct += 1

print('Total Accuracy ', complete_correct/len(y_test))
print('Character Accuracy ', chars_correct/total_chars)



# path = 'test.jpg_bounding_box.png'
# labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# im = cv2.imread(path)
# im = imutils.resize(im, width = 300)
# # convert to grayscale and blur the image
# im_grayscale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# im_blur = cv2.GaussianBlur(im_grayscale,(7,7),0)
# im_binary = cv2.threshold(im_blur, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]              
# im_binary = cv2.bitwise_not(im_binary)
# cv2.imshow('bin', im_binary)
# cv2.waitKey(0)


# contours, n = cv2.findContours(im_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = sorted(contours, key = lambda k: cv2.boundingRect(k)[0], reverse=False)


# # Initialize a list which will be used to append charater image
# character_ims= []
# for c in contours:
#     (x, y, w, h) = cv2.boundingRect(c)
#     ratio = h/w
#     if 1<=ratio<=5: # Only select contour with defined ratio
#         if h/im.shape[0]>=0.5: # Select contour which has the height larger than 50% of the plate
#             # Draw bounding box arroung digit number
#             #cv2.rectangle(test_roi, (x, y), (x + w, y + h), (0, 255,0), 2)

#             # Sperate number and gibe prediction
#             curr_num = im_binary[y:y+h,x:x+w]
#             curr_num = cv2.resize(curr_num, dsize=(60, 60))
#             curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#             character_ims.append(curr_num)

# print("Detect {} letters...".format(len(character_ims)))
# fig = plt.figure(figsize=(14,4))
# grid = gs.GridSpec(ncols=len(character_ims),nrows=1,figure=fig)

# for i in range(len(character_ims)):
#     fig.add_subplot(grid[i])
#     plt.axis(False)
#     plt.imshow(character_ims[i],cmap="gray")

# print(character_ims[0].shape)
# print(type(character_ims[0]))
# plt.show()


# model = tf.keras.models.load_model('trained_character_model')
# for im in character_ims:
#     rgb_im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
#     #print(rgb_im.shape)
#     rgb_im = np.expand_dims(rgb_im, axis = 0)
#     pred = model.predict(rgb_im)[0]
#     idx = np.argmax(pred)
#     print(labels[idx])

