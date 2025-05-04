# LILYVIOLET:  &nbsp;&nbsp; Should You Buy It?

Fastapi based web app that webscrapes review from the amazon link you provide and summarizes and classifies them tries to give an opinion about whether you should buy it or meh.<br><br>
The model is trained with SVC algo on amazon reviews dataset from kaggle. You can download it in and save the train.csv in ./DATASET URL= https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews

---

## Features

-  Speed Options:<br>
   &nbsp;&nbsp;&nbsp;&nbsp;  **Fast** – Instant Results (but unsafe, amazon can block if misused)<br>
   &nbsp;&nbsp;&nbsp;&nbsp;  **Medium** – Slower, human-like scraping<br>
   &nbsp;&nbsp;&nbsp;&nbsp;  **Slow** – Slowest for nice animation view

-  Choose number of reviews to analyze
-  Real-time logging panel
-  ML-powered summarization & sentiment prediction through SVC

---

## How it works

1. User inputs a product URL
2. Selects scraping speed and number of reviews
3. The app logs scraping activity live in a "Logging" panel
4. Once scraped, reviews are preprocessed and fed into a trained SVC model
5. Summarized reviews and predictions are returned.
6. A wordcloud is also generated for most occuring words.

---

