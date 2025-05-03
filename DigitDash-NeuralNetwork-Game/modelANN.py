import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

#loading mnist dataset(inbuitl in keras)
(train_images, train_ans), (test_images, test_ans) = tf.keras.datasets.mnist.load_data()

#making pixels:invl[0,255] into pixels:invl[0,1]
train_images=train_images.astype('float32')/255.0
test_images=test_images.astype('float32')/255.0

#reshaping image(our image is 28*28 2D matrix,flattening it out to 1*784) (so its now a 784-dimensional(columns) matrix/vector
# a mtrix is a vector when rowcount=1 isnt it
train_images=train_images.reshape(-1, 784)
test_images=test_images.reshape(-1, 784)

#converting ans to one-hot encoded format
# like if an ans is 5, converting into [0,0,0,0,0,1,0,0,0,0]
# so that our model can output a single 10 dimensional vector
train_ans=to_categorical(train_ans, num_classes=10)
test_ans=to_categorical(test_ans, num_classes=10)

#Building the model architecture 
model=Sequential([
    Dense(784, activation="relu", input_shape=(784,)),  # HL1
    Dropout(0.29),  #Dropout-layer=randomly sets 20perc of activations to 0
    Dense(256, activation="relu"),  # HL2
    Dropout(0.29),
    Dense(10, activation="softmax") 
    #since sigmoid binary classification me use hota hai
    # this is multiclass, so softmax
    # Output layer with 10 neurons(digits 0-9), like a 10dimensional vector output
])

#compiling the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',#since this a multi class classification
    metrics=['accuracy']
)
#Compiling the model=configuringhow the neural network will learn
#   optimizer=>how the model updates its weights.
#   loss fn=>how the model measure errors.
#   evaluation metric=>what performance metric to track.

#Training the model
workflow =model.fit(
    train_images,
    train_ans,
    epochs=50,
    batch_size=128,
    validation_split=0.2,  #use 20perc of training data for validation
    shuffle=True#for proper validation split
)

#evaluation of test set
test_loss, test_acc=model.evaluate(test_images, test_ans)
print(f"Test accuracy: {test_acc:.4f}")

#saving the model
model.save('mnist_ann_model.keras')

#plotting training history
plt.plot(workflow.history['accuracy'], label='Training Accuracy')
plt.plot(workflow.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()