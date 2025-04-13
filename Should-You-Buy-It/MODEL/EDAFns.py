###Exploratory Data Analysis (EDA)
from collections import Counter
import pandas as pd

from PreprocessFns import preprocess,lemmatize_text

def wordRankingDF(LIST_OF_REVIEWS):
    for i in range(len(LIST_OF_REVIEWS)):
        LIST_OF_REVIEWS[i]=lemmatize_text(preprocess(LIST_OF_REVIEWS[i]))

    all_string=" ".join(LIST_OF_REVIEWS)
    freq_per_word=Counter(all_string.split())

    word_freq_df=pd.DataFrame(freq_per_word.items(), columns=['Word', 'Frequency'])
    word_freq_df = word_freq_df[word_freq_df["Word"].apply(lambda w: w not in ["product", "amazon"])]
    word_freq_df=word_freq_df.sort_values('Frequency', ascending=False).reset_index(drop=True)

    word_freq_df['Rank']=word_freq_df.index + 1
    word_freq_df=word_freq_df[['Rank', 'Word', 'Frequency']]
    return word_freq_df

def wordCloud(word_freq_df,save_address="./static/alpha.png"):
    from wordcloud import WordCloud
    # Create a dictionary of word: frequency
    freq_dict = dict(zip(word_freq_df["Word"], word_freq_df["Frequency"]))
    # Initialize WordCloud object
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate_from_frequencies(freq_dict)
    # Save the image
    wc.to_file(save_address)

test_phrases=[
        "this bottle is not good",
        "I did not like the product",
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
df=wordRankingDF(test_phrases)
wordCloud(df)