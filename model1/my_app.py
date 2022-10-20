
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
st.write("https://archive.ics.uci.edu/ml/machine-learning-databases/magic/magic04.data")

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

def scale_dataset(dataframe, oversample=False):
    X = dataframe[dataframe.columns[:-1]].values
    y = dataframe[dataframe.columns[-1]].values
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    if oversample:
        ros = RandomOverSampler()
        X, y = ros.fit_resample(X, y)
    data = np.hstack((X, np.reshape(y, (-1, 1))))
    return data, X, y

st.write("Maintenant dans le jeu de test d'enregistrements **gamma**", len(train[train["class"] == 1]))
st.write("Maintenant, un jeu de test d'enregistrements **gudron**", len(train[train["class"] == 0]))

train, X_train, y_train = scale_dataset(train, oversample=True)
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)
test, X_test, y_test = scale_dataset(test, oversample=False)

code = """
def scale_dataset(dataframe, oversample=False):
    X = dataframe[dataframe.columns[:-1]].values
    y = dataframe[dataframe.columns[-1]].values
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    if oversample:
        ros = RandomOverSampler()
        X, y = ros.fit_resample(X, y)
    data = np.hstack((X, np.reshape(y, (-1, 1))))
    return data, X, y
"""
st.code(code, language='python')

st.write("Après avoir aligné les données dans le jeu d'enregistrements de test avec 0 et 1, il est devenu le même nombre")
st.write("Maintenant dans le jeu de test d'enregistrements **gamma**", 7399)
st.write("Maintenant, un jeu de test d'enregistrements **gudron**", 7399)

number = st.slider('Sélectionnez le nombre de points adjacents', 1, 10, 1)
st.write("Vous avez choisi ", number, ' nombre de voisins')

knn_model = KNeighborsClassifier(n_neighbors=number)
knn_model.fit(X_train, y_train)
y_pred = knn_model.predict(X_test)

result = classification_report(y_test, y_pred)
st.header("Résultat de la prédiction")
# st.table(result)
# st.dataframe(result)
result['label 1']
result['label 2']
