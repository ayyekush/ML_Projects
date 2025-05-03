import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
from random import randint

def loadModel(model_path):
    return tf.keras.models.load_model(model_path)

def showImageForReference(img,pred):
    #since image:shape(1,784), but originalshape(28,28)
    plt.imshow(img.reshape(28, 28), cmap="gray")
    plt.title(f"Predicted: {pred}")
    plt.axis("off")#we dont need axis labels
    plt.show()

def prediction(img,model):
    print("Predicted Probabilities:", model.predict(img))
    print("Predicted Class:", np.argmax(model.predict(img), axis=1))
    showImageForReference(img,np.argmax(model.predict(img), axis=1))

def predOnDatasetImage(model):
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    #making pixels:invl[0,255] into pixels:invl[0,1]
    train_images = train_images.astype('float32') / 255.0
    test_images = test_images.astype('float32') / 255.0

    #reshaping images to 784-dimensional vectors (flattening 28x28)
    train_images = train_images.reshape(-1, 784)
    test_images = test_images.reshape(-1, 784)
    i:int=randint(0,10000)
    return prediction(test_images[i].reshape(1,784),model)

def predOnCustomImageFromPath(imgPath,model):
    img=cv2.imread(imgPath,cv2.IMREAD_GRAYSCALE)  #load as grayscale(default read as 3 layers(BGR))
    img=cv2.resize(img, (28,28))  #resize to 28x28
    img=img/255.0  #normalize to [0 to 1]
    img=1-img  #inverting the colors if input is black on white back(since mnist dataset has white on black images)
    img=img.reshape(1, 784).astype("float32")
    return prediction(img,model)

if __name__=="__main__":
    model=loadModel("./mnistANNModel.keras")#path to model
    predOnCustomImageFromPath("./dalle3.webp",model)#path to test image
    predOnDatasetImage(model)#no need to pass any arg, a random image from dataset is selected
