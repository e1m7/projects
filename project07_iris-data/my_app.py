
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from PIL import Image

image0 = Image.open('0.jpg')
image1 = Image.open('1.jpg')
image2 = Image.open('2.jpg')

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

# Делаем предсказание для пользовательского набора
prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

a1, a2, a3 = st.columns(3)

a1.subheader('Class labels')
a1.write(iris.target_names)

a2.subheader('Prediction')
a2.write(iris.target_names[prediction])
st.write(prediction[0])

a2.subheader('Probability')
a2.write(prediction_proba)

# Вывод рисунка предсказанного цветка
if prediction[0] == 0:
    a3.image(image0, caption='Setosa')
elif prediction[0] == 1:
    a3.image(image1, caption='Versicolor')
else:
    a3.image(image2, caption='Virginica')
