import os
from tkinter import Label
import numpy as np
import tensorflow
from os import listdir
from keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

print('FINISHED IMPORTS')

X = []
y = []
labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
basepath = 'dataset_characters'

for label in labels:
    currdir = os.path.join(basepath, label)
    for file in listdir(currdir):
        currfile = os.path.join(currdir, file)
        image = load_img(currfile, target_size=(60,60))
        image = img_to_array(image)
        X.append(image)
        y.append(label)

print('FINISHED LOADING DATA')

X = np.array(X, dtype='float16')
y = np.array(y)

encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)
y = to_categorical(y)

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1, stratify=y)
print('FINISHED SPLITTING DATA')
######################
# Model Architecture #
######################
model = Sequential()
model.add(Conv2D(32, (3,3), input_shape=(60, 60 ,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(32, (3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(units=128, activation = 'relu'))
model.add(Dense(units=36, activation = 'softmax'))
model.compile(optimizer = 'adam', loss='categorical_crossentropy', metrics = ['accuracy'])
######################
######################

model.fit(train_X, train_y, 64, 20, 2)
model.save('trained_character_model2')