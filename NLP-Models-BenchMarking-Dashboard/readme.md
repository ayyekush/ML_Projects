# NLP Models Benchmarking Dashboard

A comprehensive dashboard for comparing and benchmarking various machine learning models on sentiment analysis tasks using real-world text data from Kindle reviews.

## Overview

The NLP Model Comparator is a web-based tool designed to evaluate and compare the performance of different machine learning models for sentiment analysis. It allows users to experiment with various text vectorization techniques and model architectures to determine which combinations yield the best results for sentiment classification tasks.

## Features

- **Multiple ML Models**: Compare performance across Logistic Regression, SVM, different Naive Bayes variants, and Neural Networks
- **Dual Vectorization Methods**: Choose between Bag of Words (BoW) and TF-IDF text representations
- **Interactive Dashboard**: Select models and vectorization techniques via an intuitive UI
- **Real-time Analysis**: Input any Kindle review text to get instant sentiment predictions
- **Performance Metrics**: View and compare accuracy, F1 scores, and confusion matrices for all model combinations
- **Visual Comparisons**: Graphical representation of model performance for easy comparison

## Models Implemented

| Model Type | Variants |
|------------|----------|
| Classical ML | Logistic Regression |
| Support Vector Machines | SVC with PCA dimensionality reduction |
| Naive Bayes | Bernoulli NB, Multinomial NB, Gaussian NB |
| Neural Networks | Artificial Neural Network (ANN) |

## Usage

1. Select a vectorization method (TF-IDF or Bag of Words)
2. Choose a model type from the dropdown
3. Paste a Kindle review in the input box
4. View the sentiment prediction results
5. Compare model performance metrics on the right panel

## Model Training

The models were trained on a dataset of Kindle reviews with binary sentiment labels (0 for negative, 1 for positive). The training code is not included in this repository, but the pre-trained models are provided.

## Performance

Performance metrics for all models are displayed in the dashboard UI, allowing for quick comparison of different approaches. Key metrics include:

- Accuracy
- F1 Score
- Confusion Matrix
