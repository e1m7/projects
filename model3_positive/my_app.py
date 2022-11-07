import streamlit as st

import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn import svm

class Sentiment:
  NEGATIVE = 'NEGATIVE'
  NEUTRAL = 'NEUTRAL'
  POSITIVE = 'POSITIVE'

class Review:
  def __init__(self, text, score):
    self.text = text
    self.score = score
    self.sentiment = self.get_sentiment()

  def get_sentiment(self):
    if self.score <= 2: return Sentiment.NEGATIVE
    elif self.score == 3: return Sentiment.NEUTRAL
    else: return Sentiment.POSITIVE

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None: df = pd.read_json(uploaded_file, names=cols)

reviews = []

with open(file_name) as f:
  for line in f:
    review = json.loads(line)
    reviews.append(Review(review['reviewText'], review['overall']))

st.title("SVM-test: Positive/Negative text")
st.write(reviews[0].text)

# training, test = train_test_split(reviews, test_size=0.33, random_state=42)

# train_x = [x.text for x in training]
# train_y = [x.sentiment for x in training]
# test_x = [x.text for x in test]
# test_y = [x.sentiment for x in test]

# vectorized = CountVectorizer()
# train_x_vectors = vectorized.fit_transform(train_x)
# test_x_vectors = vectorized.transform(test_x)

# clf_svm = svm.SVC(kernel='linear')
# clf_svm.fit(train_x_vectors, train_y)

# a = clf_svm.predict(test_x_vectors[0])
# st.write(a)

