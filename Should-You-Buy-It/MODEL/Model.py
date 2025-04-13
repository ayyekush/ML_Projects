import pandas as pd
import joblib

from PreprocessFns import preprocess,emphasise_negation,lemmatize_text
def preprocessPipelineFn():
    train_df =pd.read_csv("../DATASET/train.csv", nrows=500_000)
    train_df.columns =["Sentiment", "Title", "Review"]
    train_df=train_df.drop("Title", axis=1)

    train_df["Sentiment"]=train_df["Sentiment"].apply(lambda x: 1 if (x==2) else 0)

    train_df["Review"]=train_df["Review"].apply(preprocess)
    train_df["Review"]=train_df["Review"].apply(emphasise_negation)
    train_df["Review"]=train_df["Review"].apply(lemmatize_text)


    X_train_preprocessed=train_df['Review']
    y_train_preprocessed=train_df['Sentiment']

    return X_train_preprocessed,y_train_preprocessed

def tfidfVectorizerMaker():
    # TF-IDF vectorization
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer=TfidfVectorizer(
        max_features=5000, 
        ngram_range=(1, 3),
        max_df=0.8,#(%)    #appears in at most 85% of sents(dox) if it present more means not important
        min_df=5,#(times)  #atleast present 5 times
        sublinear_tf=True,
    )
    return tfidf_vectorizer


### Selecting a LinearSVC model via GridSearch
#       Hyperparameter tuning for LinearSVC
def selectingModel(X_train_tfidf,y_train):
    # Hyperparameter tuning
    parameters_grid = {
        'C':[0.1, 1, 10],#chosing one of the regularization parameter from this
        'class_weight':[None, 'balanced']#None->all classes are treated equally in balanced proprtionally
    }
    # Searching the best model
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import GridSearchCV
    searchingModel = GridSearchCV(
        LinearSVC(dual='auto', max_iter=10000),
        parameters_grid,
        cv=5,#five times cross validation
        scoring='f1', # F1 score is optimization metric, good for imablanced dataset
        verbose=1
    )
    #training the model for every combination of params
    searchingModel.fit(
        X_train_tfidf,
        y_train
    )
    print(f"Best parameters: {searchingModel.best_params_}")
    print(f"Best cross-validation score: {searchingModel.best_score_:.4f}")

    #having the best model
    final_chosen_model=searchingModel.best_estimator_
    return final_chosen_model

if __name__=="__main__":

    X_train,y_train=preprocessPipelineFn()

    tfidf_vectorizer=tfidfVectorizerMaker()
    X_train_tfidf=tfidf_vectorizer.fit_transform(X_train)

    final_model=selectingModel(X_train_tfidf,y_train)

    # Saving the model and vectorizer
    joblib.dump(final_model,'sentiment_model.pkl')
    joblib.dump(tfidf_vectorizer,'tfidf_vectorizer.pkl')