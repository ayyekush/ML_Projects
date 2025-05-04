import joblib
from PreprocessFns import preprocess,emphasise_negation,lemmatize_text

tfidf_vectorizer=joblib.load("./MODEL/tfidf_vectorizer.pkl")
final_svc_model=joblib.load("./MODEL/sentiment_model.pkl")

def predict_sentiment(text):
    preprocessed_text=lemmatize_text(emphasise_negation(preprocess(text)))
    text_tfidf_ed=tfidf_vectorizer.transform([preprocessed_text])

    prediction=final_svc_model.predict(text_tfidf_ed)[0]
    confidence_for_pred=abs(final_svc_model.decision_function(text_tfidf_ed)[0])

    normalized_confidence_for_pred=1/(1+2.71**(-1*confidence_for_pred))
    return prediction, normalized_confidence_for_pred

def finalPrediction(test_review_list):
    predictions=[]
    confidences=[]

    for test_review in test_review_list:
        prediction, confidence=predict_sentiment(test_review)
        predictions.append(prediction)
        confidences.append(confidence)

    min_conf=min(confidences)
    max_conf=max(confidences)

    #for 0 divi
    if max_conf==min_conf:
        normalized_confidences=[1.0]*len(confidences)
    else:
        normalized_confidences=[(c-min_conf)/(max_conf-min_conf) for c in confidences]

    total_weighted = sum(p * c for p, c in zip(predictions, normalized_confidences))
    return total_weighted / len(test_review_list)



if __name__=="__main__":
    #testing model
    test_phrases = [
        "this bottle is not good",
        "I did not like the product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "This is a great product",
        "Not bad experience at all",
        "The product is good but has some issues"
    ]
    print(finalPrediction(test_phrases))

    # for test_text in test_phrases:
    #     prediction, confidence = predict_sentiment(test_text)
    #     print(f"Text: {test_text}")
    #     print(f"Predicted sentiment: {prediction}, confidence: {confidence:.2f}")
    #     print("-" * 50)

