import pandas as pd
import re

from nltk.corpus import stopwords
stop_words_eng=stopwords.words("english")
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

def preprocess(text):
    text=text.lower()
    # Removing non-alphabets, URLs, special characters, and numbers
    text=re.sub(r'https?://\S+|www\.\S+|\[.*?\]|[^a-zA-Z\s]+|\w*\d\w*', '', text)

    #Removing stopwords
    without_stopwords=[i for i in text.split() if i not in stop_words_eng]
    return " ".join(without_stopwords).strip()

def emphasise_negation(text):
    negation_words=["not", 'no', 'barely',"doesn't",  'never',
                    'neither', 'hardly',"isn't", "wasn't", "shouldn't",
                    "wouldn't","couldn't", "won't", "can't", "don't"]
    
    transformed_words=[]
    negation_active=False
    
    for word in text.split():
        if word in negation_words:
            negation_active=True
            transformed_words.append(word)
        elif negation_active and word in ['.', '!', '?', ',', ';', ':', 'but']:
            negation_active=False
            transformed_words.append(word)
        elif negation_active:
            transformed_words.append(word+'_NEGATIVE')
        else:
            transformed_words.append(word)
    
    return ' '.join(transformed_words)

def lemmatize_text(text):
    lemmatized_words=[lemmatizer.lemmatize(word) for word in text.split()]
    return " ".join(lemmatized_words).strip()

if __name__=="__main__":
    pass
