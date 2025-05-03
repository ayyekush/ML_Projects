FROM python:3.9-slim

#setting a working dir in the container
WORKDIR /app

#installing python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copying the essential files
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/
COPY ARTIFACTS/Bow.pkl ./ARTIFACTS/
COPY ARTIFACTS/Tfidf.pkl ./ARTIFACTS/
COPY ARTIFACTS/PCAforSVC.pkl ./ARTIFACTS/
COPY ClassicalML_MODELS/ ./ClassicalML_MODELS/
COPY NaiveBayes_MODELS/ ./NaiveBayes_MODELS/
COPY SVM_MODELS/ ./SVM_MODELS/
COPY NeuralNetwork_MODELS/ ./NeuralNetwork_MODELS/



#Set and Expose the port
ENV PORT=8080
EXPOSE 8080

# Run the app when the container launches
CMD ["python", "app.py"]