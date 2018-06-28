'''
Script for creating testing and validating database.
It parses data from CKP and MMI databases.

Author: Adriana Tufa
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
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    # img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    # img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    # img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])


    # dst = copy(img)
    # img = cv2.normalize(img, dst, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return img


def make_datum(img, label):
    #image is numpy.ndarray format. BGR instead of RGB
    #rollaxis to channge from (227, 227, 3) to (3, 227, 227)

    return caffe_pb2.Datum(
        channels=3,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        label=label,
        data=np.rollaxis(img, 2).astype(np.uint8).tostring())

def detect_face(img_path):
    face_cascade = cv2.CascadeClassifier('/home/adriana/Documents/emotion-train/code/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = img

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    if len(faces) > 1:
        print 'mai multe'

    (x, y, w, h) = faces[0]

    img = img[y : y + h, x : x + w]
    img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT),  interpolation=cv2.INTER_CUBIC)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    return img

def change_label(label):
    if label == 0:
        return 4
    if label == 1:
        return 0
    if label == 2:
        return 1
    if label == 3:
        return 2
    if label == 4:
        return 3
    return label

train_lmdb = '/home/adriana/Documents/emotion-train/input/gil_train_lmdb'
validation_lmdb = '/home/adriana/Documents/emotion-train/input/gil_validation_lmdb'

os.system('rm -rf  ' + train_lmdb)
os.system('rm -rf  ' + validation_lmdb)

# Prepare CKP
image_folders_ckp = glob.glob('/home/adriana/Documents/emotion-train/input/photos/*/*')
image_paths_ckp = [] # list of (image_path, label)

all_image_paths = []

neutral_subjects = []

# Get the last half of images from every folder
for img_folder in image_folders_ckp:
    aux = img_folder.split('/')
    images = glob.glob(img_folder + '/*png')
    images.sort()
    nr_img = len(images)

    label_path = '/home/adriana/Documents/emotion-train/input/labels/' + aux[-2] + '/' + aux[-1] +'/*'
    label_filename = glob.glob(label_path)
    if len(label_filename) > 0:
        label_filename = label_filename[0]
    else:
        continue

    label_file = open(label_filename)
    label_str = label_file.read().split('.')[0]

    label = int(label_str)
    if label == 2:
            continue # disregard contempt
    if label >= 3:
        label = label - 1

    label  = change_label(label)

    for img_path in images[-1 :]:
        image_paths_ckp.append((img_path, label))
        all_image_paths.append((img_path, label))

    # append neutral photo; only one for every subject
    if aux[-2] not in neutral_subjects:
        image_paths_ckp.append((images[0], 4))
        all_image_paths.append((images[0], 4))
        neutral_subjects.append(aux[-2])


random.shuffle(image_paths_ckp)
print 'CKP ' + str(len(image_paths_ckp)) + ' images'
l = len(image_paths_ckp) / 5
train_data_ckp = image_paths_ckp[ : 4 * l]
test_data_ckp = image_paths_ckp[4 * l : ]

# MMI
image_paths_mmi = glob.glob('/home/adriana/Documents/emotion-train/input/mmi_photos/*/*')
random.shuffle(image_paths_mmi)
print 'MMI ' + str(len(image_paths_mmi)) + ' images'
l = len(image_paths_mmi) / 5
train_data_mmi = image_paths_mmi[:4 * l]
test_data_mmi = image_paths_mmi[4 * l:]

for img_path in image_paths_mmi:
    emotion = img_path.split('/')[-2]
    label = int(emotion)

    label = change_label(label)

    all_image_paths.append((img_path, label))

random.shuffle(all_image_paths)
l = len(all_image_paths) / 5
train_data = all_image_paths[: 4 * l]
test_data = all_image_paths[4 * l :]


print 'Creating train_lmdb'
count = 0
classes = {}
for i in range(7):
    classes[i] = 0

in_db = lmdb.open(train_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:

    for (img_path, label) in train_data:

        img = detect_face(img_path)
        if img == None:
            print "face not detected"
            continue

        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

        count += 1
        classes[label] += 1

        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(count), datum.SerializeToString())

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

    for (img_path, label) in test_data:

        img = detect_face(img_path)
        if img == None:
            print "face not detected"
            continue

        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

        count += 1
        classes[label] += 1
        
        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(count), datum.SerializeToString())

in_db.close()


print 'labeled ' + str(count) + ' photos'
for (a,b) in classes.items():
    print 'Clasa ' + str(a) + ' cu ' + str(b)

print '\nFinished processing all images'

print '\nGenerating mean..'
os.system('bash gil_generate_mean.sh')
