import numpy as np                                  # Needed to work with arrays

from os.path import exists                # Needed to check if mnist files exist
from os import mkdir, system, listdir                # Needed for interaction with the os
import scipy.io
import scipy.misc

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import pylab
import cPickle

CIFAR_PATH = "./CIFAR"
CIFAR_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
CIFAR_ARCH = "cifar-10-python.tar.gz"
CIFAR_TRAIN_FILES = [
    "data_batch_1",
    "data_batch_2",
    "data_batch_3",
    "data_batch_4",
    "data_batch_5"]
CIFAR_TEST_FILE = "test_batch"

CFK_URL = "http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/EnglishImg.tgz" 
CFK_ARCH = "EnglishImg.tgz"
CFK_PATH = "./CFK"

def preprocess(train_imgs, test_imgs):
    for dim in range(3):
        avg = np.mean(train_imgs[:, dim])
        
        train_imgs[:, dim] -= avg
        test_imgs[:, dim] -= avg

        dev = np.std(train_imgs[:, dim])
        train_imgs[:, dim] /= dev
        test_imgs[:, dim] /= dev




def download_cifar():
    system("wget %s" % CIFAR_URL)
    system("tar -xf %s" % CIFAR_ARCH)
    system("mv cifar-10-batches-py %s" % CIFAR_PATH)
    system("rm %s" % CIFAR_ARCH)


def load_cifar():
    data = {"train_labels": []}
    for fname in CIFAR_TRAIN_FILES:
        f = open(CIFAR_PATH + "/" + fname)
        fdata = cPickle.load(f)
        f.close()
        
        print fdata["data"].shape
        print len(fdata["labels"])
        if "train_imgs" not in data:
            data["train_imgs"] = fdata["data"].reshape(10000, 3, 32, 32) / 255.0
            
            # plt.imshow(data["train_imgs"][0].transpose(2,1 , 0), interpolation="nearest")
            # plt.pause(30)
        else:
            data["train_imgs"] = np.concatenate((data["train_imgs"], fdata["data"].reshape(10000, 3, 32, 32)/ 255.0), axis=0)
        data["train_labels"] += fdata["labels"]

        # X = fdata["data"].reshape(10000, 3, 32, 32).transpose(0,2,3,1)
        # fig, axes1 = plt.subplots(5,5,figsize=(3,3))
        # for j in range(5):
        #     for k in range(5):
        #         i = np.random.choice(range(len(X)))
        #         axes1[j][k].set_axis_off()
        #         axes1[j][k].imshow(X[i])
        # plt.pause(10)

    f = open(CIFAR_PATH + "/" + CIFAR_TEST_FILE)
    fdata = cPickle.load(f)
    f.close()

    data["test_imgs"] = fdata["data"].reshape(10000, 3, 32, 32) / 255.0
    data["test_labels"] = fdata["labels"]

    preprocess(data["train_imgs"], data["test_imgs"])

    data["train_no"] = len(CIFAR_TRAIN_FILES) * 10000
    data["test_no"] = 10000

    return data

def download_cfk():
    system("wget %s" % CFK_URL)
    system("tar -xf %s" % CFK_ARCH)
    system("mv English %s" % CFK_PATH)
    system("rm %s" % CFK_ARCH)

    system("wget http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/Lists.tgz")
    system("tar -xf Lists.tgz")
    system("mv Lists %s" % CFK_PATH)

def load_cfk():
    res = scipy.io.loadmat("CFK/Lists/English/Img/lists.mat")["list"]
    main_dir = "CFK/Img/"
    img_size = (32, 32)

    data = {"train_labels": [], "test_labels": []}
    cnt = 0

    for i, img_dir in enumerate(res["classnames"][0][0]):
        crt_dir = main_dir + str(img_dir)
        files = listdir(crt_dir)

        for name in files:

            pixels = scipy.misc.imread(crt_dir + "/" + name, mode="RGB")
            pixels = scipy.misc.imresize(pixels, (32, 32), interp="cubic")
            # plt.imshow(pixels)
            # plt.pause(5)
            pixels = pixels.transpose(2, 0, 1) / 255.0

            if cnt % 5 == 0:
                if "test_imgs" not in data:
                    data["test_imgs"] = np.array([pixels])
                else:
                    data["test_imgs"] = np.concatenate((data["test_imgs"], np.array([pixels])), axis=0)
                data["test_labels"].append(i - 1)
            else:
                if "train_imgs" not in data:
                    data["train_imgs"] = np.array([pixels])
                else:
                    data["train_imgs"] = np.concatenate((data["train_imgs"], np.array([pixels])), axis=0)
                data["train_labels"].append(i - 1)

            cnt += 1

    data["train_no"] = len(data["train_labels"])
    data["test_no"] = len(data["test_labels"])

    return data

if __name__ == "__main__":

    # DONE
    # download_cifar() 
    # data = load_cifar()

    # download_cfk()
    data = load_cfk()
    # print data["train_imgs"].shape
    # print data["test_imgs"].shape
    # print data["train_labels"].shape




