
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import plotly.figure_factory as ff

st.title("K-Nearest Neighbor")
cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, names=cols)

st.write("Afficher la date d'origine à l'écran")
st.dataframe(df.head(3))

df["class"] = (df["class"] == "g").astype(int)

st.write("Dans la Dernière colonne, remplacez les valeurs 'g| / 'h' par 0/1 afin que les modèles puissent les gérer facilement")
st.dataframe(df.head(3))

st.write("Divisons le DataSet")
st.write("""
- train = données d'entraînement, 0 à 60% des données
- valid = données validées, 60 à 80% des données
- test = données de test, 80 à 100% des données
""")
train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])
st.write(train)
st.write(valid)
st.write(test)