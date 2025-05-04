import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import keras
from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Dropout,Flatten
from keras.models import load_model
from random import randint
accuracy_list=[]
pred=0
predCorrectList=[]
# Constants
EPOCHS=20
NUM_CLASSES=43

train_df=pd.read_csv("./Dataset/Train.csv")
test_df=pd.read_csv("./DATASET/Test.csv")
# train_df.shape #(39209,8)

Meta_df=pd.read_csv("./Dataset/Meta.csv")
Meta_df=Meta_df.drop("ShapeId",axis=1).drop("ColorId",axis=1).drop("SignId",axis=1)
Meta_DICT={i:val for i,val in zip(Meta_df["ClassId"],Meta_df["Path"])}

def PreparingData(train_df, test_df, model_choice):
    # TRAINING DATA
    train_images=[]
    train_images_labels=[]
    for i in range(train_df.shape[0]):
        #convert("L") for grayscale
        #if RGB, layers(3rd_dim)=3 but for grayscale you
        #   have to explicitly increase dim for 3rd_dim=1
        if (model_choice=="L"):
            img=Image.open("./DATASET/"+train_df["Path"][i]).convert("L")
        elif (model_choice=="RGB"):
            img=Image.open("./DATASET/"+train_df["Path"][i])
        else:
            return False
        img=img.resize((30,30))
        img=np.array(img,dtype=np.float32)/255.0
        if (model_choice=="L"):
            img=np.expand_dims(img,axis=-1)# for grayscale
        #expand dims sirf pred ke wakt kyuki training ke
        #   wakt usme batch_no dim ko add kar dete hain
        train_images.append(img)
        train_images_labels.append(train_df["ClassId"][i])
    print("reacachd")
    train_images=np.array(train_images)
    train_images_labels=np.array(train_images_labels)
    # data.shape,labels.shape #((39209, 30, 30, 3), (39209,))
    #output toh NUM_CLASSES honge na labels ka shape toh abhi
    #   (39209,) hai. isko OHE karke (39209,NUM_CLASSES)
    from keras.utils import to_categorical
    train_images_labels=to_categorical(train_images_labels,NUM_CLASSES)
    # print(train_images_labels.shape) #(39209, 43)

    # TESTING DATA
    test_img_labels=test_df["ClassId"]
    from tensorflow.keras.utils import to_categorical
    test_images_labels=to_categorical(test_img_labels,NUM_CLASSES)

    test_img_paths=pd.read_csv("./DATASET/Test.csv")["Path"]
    test_images=[]
    for i in range(len(test_img_labels)):
        img=Image.open("./DATASET/"+test_img_paths.iloc[i]).convert("L")
        img=img.resize((30,30))
        img=np.array(img,dtype=np.float32)/255.0
        img=np.expand_dims(img,axis=-1)
        test_images.append(img)
    test_images=np.array(test_images)

    return (train_images, train_images_labels, test_images, test_images_labels)

def BuildModel(train_images,train_images_labels, test_images,test_images_labels, model_choice="L"):
    print("reached herer")
    model=Sequential()
    model.add(keras.Input(train_images.shape[1:]))
    model.add(Conv2D(32,(5,5),activation="relu"))
    model.add(Conv2D(32,(5,5),activation="relu"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(rate=0.2))
    model.add(Conv2D(64,(3,3),activation="relu"))
    model.add(Conv2D(64,(3,3),activation="relu"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(rate=0.2))
    model.add(Flatten())#None,3,3,64->None,3*3*64
    model.add(Dense(576,activation="relu"))
    model.add(Dropout(rate=0.5))
    model.add(Dense(NUM_CLASSES,activation="softmax"))
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )
    # trainHistory=model.fit(
    #     train_images,
    #     train_images_labels,
    #     batch_size=32,
    #     epochs=10,
    #     validation_data=(test_images,test_images_labels)
    # )
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        brightness_range=[0.8, 1.2],
        horizontal_flip=False,  # Don't flip traffic signs horizontally
        fill_mode='nearest'
    )
    
    trainHistory=model.fit(
        datagen.flow(train_images, train_images_labels, batch_size=32),
        epochs=EPOCHS,
        steps_per_epoch=len(train_images) // 32,
        validation_data=(test_images, test_images_labels)
    )
    model.save(f"./MODELS/RNN_Traffic_{model_choice}4.keras")
    return (model,trainHistory)


if __name__=="__main__":
    model_choice="L" or "RGB"
    BuildModel(*PreparingData(train_df,test_df,model_choice),model_choice)
