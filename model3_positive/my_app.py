import streamlit as st

import pandas as pd
import numpy as np

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

st.write(reviews[0].text)
