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

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


def make_datum(img, label):
    #image is numpy.ndarray format. BGR instead of RGB
    return caffe_pb2.Datum(
        channels=3,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        label=label,
        data=np.rollaxis(img, 2).tostring())

train_lmdb = '/home/adriana/Documents/emotion-train/input/train_lmdb'
validation_lmdb = '/home/adriana/Documents/emotion-train/input/validation_lmdb'

os.system('rm -rf  ' + train_lmdb)
os.system('rm -rf  ' + validation_lmdb)


images = [img for img in glob.glob('/home/adriana/Documents/emotion-train/input/photos/*/*/*png')]
print (len(images))

random.shuffle(images)
train_data = images[0:8500]
test_data = images[8500:]

classes = {}
for i in range(7):
    classes[i] = 0


print 'Creating train_lmdb'
count = 0

in_db = lmdb.open(train_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, img_path in enumerate(train_data):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

        # get label
        aux = img_path.split('/')[-3:-1]
        label_path = '/home/adriana/Documents/emotion-train/input/labels/' + aux[0] + '/' + aux[1] + '/*'
        label_filename = glob.glob(label_path)
        if len(label_filename) > 0:
            label_filename = label_filename[0]
            count += 1
        else:
            continue
        label_file = open(label_filename)
        label_str = label_file.read().split('.')[0]
        label = int(label_str) - 1
        classes[label] += 1

        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
        #print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()

print 'labeled ' + str(count) + ' photos'
for (a,b) in classes.items():
    print 'Clasa ' + str(a) + ' cu ' + str(b)


print '\nCreating validation_lmdb'

count = 0
for i in range(7):
    classes[i] = 0

in_db = lmdb.open(validation_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, img_path in enumerate(test_data):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

        # get label
        aux = img_path.split('/')[-3:-1]
        label_path = '/home/adriana/Documents/emotion-train/input/labels/' + aux[0] + '/' + aux[1] + '/*'
        label_filename = glob.glob(label_path)
        if len(label_filename) > 0:
            label_filename = label_filename[0]
            count += 1
        else:
            continue
        label_file = open(label_filename)
        label_str = label_file.read().split('.')[0]
        label = int(label_str) - 1
        classes[label] += 1

        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
        #print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()
print 'labeled ' + str(count) + ' photos'

print '\nFinished processing all images'

for (a,b) in classes.items():
    print 'Clasa ' + str(a) + ' cu ' + str(b)
