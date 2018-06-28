'''
Title           :create_lmdb.py
Description     :This script divides the training images into 2 sets and stores them in lmdb databases for training and validation.
Author          :Adil Moujahid
Date Created    :20160619
Date Modified   :20160625
version         :0.2
usage           :python create_lmdb.py
python_version  :2.7.11
'''
import sys
sys.path.append("/home/adriana/Programs/caffe/python") 

import os
import glob
import random
import numpy as np

import cv2

import caffe
from caffe.proto import caffe_pb2
import lmdb
from copy import copy

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img = cv2.equalizeHist(img)

    # dst = copy(img)
    # img = cv2.normalize(img, dst, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return img


def make_datum(img, label):
    #image is numpy.ndarray format. BGR instead of RGB

    return caffe_pb2.Datum(
        channels=1,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        label=label,
        data=img.astype(np.uint8).tostring())

def detect_face(img_path):
    face_cascade = cv2.CascadeClassifier('/home/adriana/Documents/emotion-train/code/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img, 1.3, 5)

    if len(faces) == 0:
        return None
    (x, y, w, h) = faces[0]
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    img = img[y : y + h, x : x + w]
    img = cv2.resize(img, (227, 227),  interpolation=cv2.INTER_CUBIC)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    return img

train_lmdb = '/home/adriana/Documents/emotion-train/input/train_lmdb'
validation_lmdb = '/home/adriana/Documents/emotion-train/input/validation_lmdb'

os.system('rm -rf  ' + train_lmdb)
os.system('rm -rf  ' + validation_lmdb)


image_folders = [img for img in glob.glob('/home/adriana/Documents/emotion-train/input/photos/*/*')]
print (len(image_folders))

random.shuffle(image_folders)
train_data = image_folders[0:494]
test_data = image_folders[494:]


print 'Creating train_lmdb'
count = 0
classes = {}
for i in range(7):
    classes[i] = 0

in_db = lmdb.open(train_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for img_folder in train_data:
        aux = img_folder.split('/')
        images = glob.glob(img_folder + '/*png')
        images.sort()
        label_path = '/home/adriana/Documents/emotion-train/input/labels/' + aux[-2] + '/' + aux[-1] +'/*'
        label_filename = glob.glob(label_path)
        if len(label_filename) > 0:
            label_filename = label_filename[0]
        else:
            continue
        label_file = open(label_filename)
        label_str = label_file.read().split('.')[0]
        label = int(label_str) - 1

        nr_img = len(images)
        for img_path in images[nr_img/2:]:
            img = detect_face(img_path)
            if img == None:
                print "face not detected"
                continue
            img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
            count += 1
            classes[label] += 1
            datum = make_datum(img, label)
            in_txn.put('{:0>5d}'.format(count), datum.SerializeToString())
            # if label == 3:
            #     print '{:0>5d}'.format(count) + ':' + img_path
in_db.close()

print 'labeled ' + str(count) + ' photos'
for (a,b) in classes.items():
    print 'Clasa ' + str(a) + ' cu ' + str(b)


print '\nCreating validation_lmdb'

count = 0
classes = {}
for i in range(7):
    classes[i] = 0
in_db = lmdb.open(validation_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for img_folder in test_data:
        aux = img_folder.split('/')
        images = glob.glob(img_folder + '/*png')
        images.sort()
        label_path = '/home/adriana/Documents/emotion-train/input/labels/' + aux[-2] + '/' + aux[-1] +'/*'
        label_filename = glob.glob(label_path)
        if len(label_filename) > 0:
            label_filename = label_filename[0]
        else:
            continue
        label_file = open(label_filename)
        label_str = label_file.read().split('.')[0]
        label = int(label_str) - 1

        nr_img = len(images)
        for img_path in images[nr_img/2:]:
            img = detect_face(img_path)
            if img == None:
                print "face not detected"
                continue
            img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
            count += 1
            classes[label] += 1
            datum = make_datum(img, label)
            in_txn.put('{:0>5d}'.format(count), datum.SerializeToString())
            #print '{:0>5d}'.format(count) + ':' + img_path
in_db.close()


print '\nFinished processing all images'

print 'labeled ' + str(count) + ' photos'
for (a,b) in classes.items():
    print 'Clasa ' + str(a) + ' cu ' + str(b)
