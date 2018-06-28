import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("/home/adriana/Programs/caffe/python") 
import caffe
import cv2
from caffe.proto import caffe_pb2

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = '/home/adriana/Documents/emotion-train/caffe_models/caffe_model_2/caffenet_deploy_2.prototxt'
PRETRAINED = '/home/adriana/Documents/emotion-train/caffe_models/caffe_model_2/snapshot_iter_1000.caffemodel'
MEAN = '/home/adriana/Documents/emotion-train/input/mean.binaryproto'


'''
Image processing helper function
'''
'''
Image processing helper function
'''
def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):
    #Histogram Equalization
    # img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    # img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    # img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    # img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    img[:, :, 0] = np.divide(img[:, :, 0], 255.0) - 0.5
    img[:, :, 1] = np.divide(img[:, :, 1], 255.0) - 0.5
    img[:, :, 2] = np.divide(img[:, :, 2], 255.0) - 0.5
    return img

def detect_face(img_path):
    face_cascade = cv2.CascadeClassifier('/home/adriana/Documents/emotion-train/code/haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = img

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

    return img

#Read mean image
mean_blob = caffe_pb2.BlobProto()
with open('/home/adriana/Documents/emotion-train/input/mean.binaryproto') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))

# load the model
caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=mean_array,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(IMAGE_WIDTH, IMAGE_HEIGHT))
print "successfully loaded classifier"

# test on a image
img_path = '/home/adriana/Documents/emotion-train/code/test.jpg'
img = detect_face(img_path)
if img == None:
  print "No face detected"
img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
# img = cv2.imread(img_path, cv2.IMREAD_COLOR)
# img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
# predict takes any number of images,
# and formats them for the Caffe net automatically
pred = net.predict([img])

print(pred)