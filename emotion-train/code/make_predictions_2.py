'''
Title           :make_predictions_2.py
Description     :This script makes predictions using the 2nd trained model and generates a submission file.
Author          :Adil Moujahid
Date Created    :20160623
Date Modified   :20160625
version         :0.2
usage           :python make_predictions_2.py
python_version  :2.7.11
'''

import os
import glob
import cv2
import lmdb
import numpy as np
import sys
sys.path.append("/home/adriana/Programs/caffe/python")
import caffe
from caffe.proto import caffe_pb2
from copy import copy

caffe.set_mode_gpu() 

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227


'''
Image processing helper function
'''
def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):
    #Histogram Equalization
    # img = cv2.equalizeHist(img)
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

 
    # dst = copy(img)
    # img = cv2.normalize(img, dst, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return img

def detect_face(img_path):
    face_cascade = cv2.CascadeClassifier('/home/adriana/Documents/emotion-train/code/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
  
    # Transform in BW  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.rollaxis(img, 2)

    # cv2.imshow('i', gray)
    # cv2.waitKey(0)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #print (str(len(faces)) + " detected")
    if len(faces) == 0:
        return None
    (x, y, w, h) = faces[0]
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    img = img[y : y + h, x : x + w]
    img = cv2.resize(img, (227, 227),  interpolation=cv2.INTER_CUBIC)

    cv2.imshow('img', img)
    cv2.waitKey(0)

    return img.astype(np.uint8)


'''
Reading mean image, caffe model and its weights 
'''
#Read mean image
# mean_blob = caffe_pb2.BlobProto()
# with open('/home/adriana/Documents/emotion-train/input/mean.binaryproto') as f:
#     mean_blob.ParseFromString(f.read())
# mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
#     (mean_blob.channels, mean_blob.height, mean_blob.width))


# # #Read model architecture and trained model's weights
# net = caffe.Net('/home/adriana/Documents/emotion-train/caffe_models/caffe_model_2/caffenet_deploy_2.prototxt',
#                 '/home/adriana/Documents/emotion-train/caffe_models/caffe_model_2/snapshot_iter_2000.caffemodel',
#                 caffe.TEST)

# # #Define image transformers
# transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# transformer.set_mean('data', mean_array)
# transformer.set_transpose('data', (2,0,1))


'''
Making predicitions
'''
##Reading image paths
test_img_paths = [img_path for img_path in glob.glob("/home/adriana/Documents/emotion-train/input/test/*jpg")]

test_ids = []
preds = []

#Making predictions
for img_path in test_img_paths:
    img = detect_face(img_path)
    if img == None:
        print "No face detected"
        continue
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

    # net.blobs['data'].data[...] = transformer.preprocess('data', img)
    # out = net.forward()
    # pred_probas = out['prob']
    # print pred_probas
    # print img_path
    # print pred_probas.argmax()
    # print '-------'

