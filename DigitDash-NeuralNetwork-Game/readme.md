# Digit Dash

Digit Dash is an interactive web-based game that showcases the power of machine learning for handwritten digit recognition. Players can draw digits on a canvas, which are then recognized in real-time using neural network architectures (CNN and ANN) trained on the MNIST dataset. The game also includes a global leaderboard to track top performers.

## 🧠 Machine Learning Components

### Neural Network Architectures

The project implements and compares two different neural network architectures:

#### 1. Artificial Neural Network (ANN)
- **Architecture**: Multi-layer perceptron with dense layers
- **Layers**:
  - Input layer: 784 neurons (flattened 28×28 images)
  - Hidden layer 1: 784 neurons with ReLU activation and 29% dropout
  - Hidden layer 2: 256 neurons with ReLU activation and 29% dropout
  - Output layer: 10 neurons with softmax activation
- **Performance**: Achieves high accuracy on the MNIST test set
- **Features**: Regularization through dropout to prevent overfitting

#### 2. Convolutional Neural Network (CNN)
- **Architecture**: Deep CNN with batch normalization
- **Layers**:
  - Multiple Convolutional layers (32 and 64 filters)
  - Batch Normalization after each convolution
  - MaxPooling to reduce spatial dimensions
  - Dropout layers (20%)
  - Dense layer with 256 neurons
  - Output layer with 10 neurons (softmax)
- **Data Augmentation**: Uses ImageDataGenerator for:
  - Rotation (±10°)
  - Width/height shifts (10%)
  - Zoom variation (10%)
- **Training**: Implements early stopping to prevent overfitting

### Model Training Process

- **Dataset**: Standard MNIST handwritten digits (60,000 training, 10,000 test images)
- **Preprocessing**: Normalization of pixel values (0-255 → 0-1)
- **Training**:
  - ANN: 50 epochs with 20% validation split
  - CNN: Up to 30 epochs with early stopping based on validation accuracy
- **Optimization**: Both models use Adam optimizer with categorical crossentropy loss
- **Evaluation**: Models are evaluated on the MNIST test set for accuracy

## 🚀 Features

- Real-time digit recognition from hand-drawn input
- Switch between ANN and CNN models for comparison
- Interactive drawing canvas 
- Global leaderboard to track top scores
- Responsive web interface

## 💻 Technology Stack

- **Backend**: FastAPI with Python
- **ML Framework**: TensorFlow/Keras
- **Frontend**: HTML/CSS/JavaScript
- **Image Processing**: PIL (Python Imaging Library)
- **Data Handling**: NumPy, JSON

## 📊 Performance Comparison

The project allows for direct comparison between traditional ANNs and CNNs for image recognition tasks:

- **ANN**: Simpler architecture, faster training, but generally lower accuracy
- **CNN**: More complex, better at capturing spatial features in images, higher accuracy