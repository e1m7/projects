
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Simple Iris Flower Prediction App

This app predicts the **Iris flower** type
""")

st.sidebar.header('User Input Parameters')

# Собираем данные от пользователя (pandas дата-сет)
def user_input_features():
    sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)      # min/max/current
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Дата-сет пользовательских данных
df = user_input_features()

st.subheader('User Input parameters')
st.write(df)

# Загружаем дата-сет про ирисы
iris = datasets.load_iris()
X = iris.data
Y = iris.target

# Создаем и тренируем модель
clf = RandomForestClassifier()
clf.fit(X, Y)

# Делаем предсказание для пользоательского набора
prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

a1, a2, a3 = st.columns(3)

a1.subheader('Class labels')
a1.write(iris.target_names)

a2.subheader('Prediction')
a2.write(iris.target_names[prediction])
st.write(prediction[0])

a3.subheader('Probability')
a3.write(prediction_proba)