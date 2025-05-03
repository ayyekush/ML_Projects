from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceOl

import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

##This is a trial to make MNIST handwritten predictor using
    #Conolutional Neural Networks.

#loading mnist dataset(inbuitl in keras)
(train_images, train_ans),(test_images, test_ans)=tf.keras.datasets.mnist.load_data()

#making pixels:invl[0,255] into pixels:invl[0,1]
train_images=train_images.astype('float32')/255.0
test_images=test_images.astype('float32')/255.0

# Reshaping images to (28x28x1) for adding color domension
train_images =train_images.reshape(-1, 28, 28, 1)
test_images=test_images.reshape(-1, 28, 28, 1)

#convert answers to ohe
train_ans=to_categorical(train_ans,num_classes=10)
test_ans= to_categorical(test_ans,num_classes=10)

from tensorflow.keras.preprocessing.image import ImageDataGenerator

#training ke liye data augmentation(artificially increase the size and diversity )
#  images ko randomly modify  taki model zyada generalize ho sake
datagen=ImageDataGenerator(
    rotation_range=10,  #Image ko -10 se +10 degrees ke beech randomly rotate
                        #makes model ready for some rotated images
    width_shift_range=0.1, #image ko horizontal direction me 10% tak left ya right shift
                            #isse model chhoti horizontal movements ko samajhne lagta hai

    height_shift_range=0.1,#images ko vertical direction me 10% tak up ya down shift
                            #for vertical variation

    zoom_range=0.1,#images ko 10% tak randomly zoom in ya zoom out
)

datagen.fit(train_images)#fitting the trainimages

#main cnn model
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
    BatchNormalization(),#normalises output of previous layer
    Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),
    
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),
    
    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),
    Dense(10, activation='softmax')  # Output layer for 10 digits
])

#compiling the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#callbacks for early stopping
early_stopping=EarlyStopping(
    monitor='val_accuracy',
    patience=10,
    restore_best_weights=True
)

#final model training
workflow =model.fit(
    datagen.flow(train_images, train_ans, batch_size=128),
    epochs=30,
    validation_data=(test_images, test_ans),#testt data for validation
    callbacks=[early_stopping]
)

#evaluation on test set
test_loss,test_acc =model.evaluate(test_images, test_ans)
print(f"Test accuracy: {test_acc:.4f}")

#finally saving the model
model.save('mnistCNNModel.keras')

#plotting the graphs
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(workflow.history['accuracy'], label='Training Accuracy')
plt.plot(workflow.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(workflow.history['loss'], label='Training Loss')
plt.plot(workflow.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()