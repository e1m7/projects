
import streamlit as st

st.title("The mood of the text")

st.write("""
Cet exemple montre comment créer et former cinq modèles d'apprentissage automatique qui peuvent identifier les émotions d'un texte (négatif, positif). Les données représentent 10.000 critiques du site Amazon

- [link](https://colab.research.google.com/drive/18M4lccM2z_-9kFcZFW5iBlQbhzIsR2gR?usp=sharing)
- [data 1000](https://drive.google.com/file/d/130JMSzxRun6TTEhrUsKTbI45Q_tlajlG/view?usp=sharing)
- [data 10000](https://drive.google.com/file/d/1a0Buhd1pzruUGDC4QC_yIV1akWIQFc2J/view?usp=sharing)
- [model](https://drive.google.com/file/d/15qL9AXJLdKy8AbNgqncdtuO28IrFlgB4/view?usp=sharing)
""")

import random
import json

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Класс настроения рецензии, состав: 1) негатив, 2) нейтральное, 3)позитив
# Classe d'humeur, composition: 1) négatif, 2) neutre, 3) positif

class Sentiment:
  NEGATIVE = 'NEGATIVE'
  NEUTRAL = 'NEUTRAL'
  POSITIVE = 'POSITIVE'

# Класс обычная рецензия, состав: 1) текст, 2) оценка, 3) настроение
# Classe, composition: 1) texte, 2) évaluation, 3) humeur

class Review:
  def __init__(self, text, score):
    self.text = text
    self.score = score
    self.sentiment = self.get_sentiment()

  # Получение настроения: 1-2 негатив, 3 нейтральное, 4-5 позитив
  # Obtenir l'humeur: 1-2 négatif, 3 neutre, 4-5 positif

  def get_sentiment(self):
    if self.score <= 2: return Sentiment.NEGATIVE
    elif self.score == 3: return Sentiment.NEUTRAL
    else: return Sentiment.POSITIVE

# Класс выровненная рецензия: число позитивных = число негативных
# Classe: nombre positif = nombre négatif

class ReviewContainer:
  def __init__(self, reviews):
    self.reviews = reviews

  def get_text(self):
    return [x.text for x in self.reviews]

  def get_sentiment(self):
    return [x.sentiment for x in self.reviews]

  # Функция выравнивания: берем негативные тексты, позитивные тексты (как списки)
  # Функция выравнивания: берем позитивных сколько негативных, склеиваем, перемешиваем
  # Fonction d'alignement: prendre des textes négatifs, textes positifs (comme des listes)
  # Fonction d'alignement: prendre positif combien négatif, coller, remuer

  def evenly_distribute(self):
    negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))
    positive = list(filter(lambda x: x.sentiment == Sentiment.POSITIVE, self.reviews))
    positive_shrunk = positive[:len(negative)]
    self.reviews = negative + positive_shrunk
    random.shuffle(self.reviews)

# Открываем файл с данными, читаем их в (обычные) рецензии
# Ouvrez le fichier avec les données, lisez - les dans les critiques (ordinaires) 

file_name = './Books_small_10000.json'
reviews = []

with open(file_name) as f:
  for line in f:
    review = json.loads(line)
    reviews.append(Review(review['reviewText'], review['overall']))

# Делим исходный датасет на два набора: 1) тренировка, 2) тестирование
# Divisez la date d'origine en deux ensembles: 1) entraînement, 2) test

training, test = train_test_split(reviews, test_size=0.33, random_state=42)

# Создаем на его основе новые контейнеры для моделей, где выровнены негатив и позитив
# Nous créons sur sa base de nouveaux conteneurs pour les modèles où le négatif et le positif sont alignés

training_container = ReviewContainer(training)
test_container = ReviewContainer(test)

# train_x = тренировочные тексты
# train_y = тренировочные настроения
# train_x = textes d'entraînement
# train_y = humeur d'entraînement

training_container.evenly_distribute()
train_x = training_container.get_text()
train_y = training_container.get_sentiment()

test_container.evenly_distribute()
test_x = test_container.get_text()
test_y = test_container.get_sentiment()

print("\nEnsemble d'entraînement")
print(train_y.count(Sentiment.POSITIVE))
print(train_y.count(Sentiment.NEGATIVE))

print("\nKit de test")
print(test_y.count(Sentiment.POSITIVE))
print(test_y.count(Sentiment.NEGATIVE))

# Разбить наборы текста на векторы: 1) как есть, 2) с анализом частотности слов
# Diviser les ensembles de texte en vecteurs: 1) tel quel, 2) avec l'analyse de la fréquence des mots

# vectorized = CountVectorizer()
vectorized = TfidfVectorizer()

# Разбить тренировочный и тестовый наборы текстов
# Briser les ensembles de textes d'entraînement et de test

train_x_vectors = vectorized.fit_transform(train_x)
test_x_vectors = vectorized.transform(test_x)

from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# Линейная модель тип SVM
# Modèle linéaire type SVM
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors, train_y)

# Модель типа дерево решений
# Modèle de type arbre de décision
clf_dec = DecisionTreeClassifier()
clf_dec.fit(train_x_vectors, train_y)

# Модель типа наивный байес
# Modèle de type naïf Bayes
clf_gnb = GaussianNB()
clf_gnb.fit(train_x_vectors.toarray(), train_y)

# Модель типа логическая регрессия
# Modèle de type régression logique
clf_log = LogisticRegression()
clf_log.fit(train_x_vectors, train_y)

# Модель типа поиск по сетке
# Modèle de type recherche par grille
parameters = { 'kernel': ('linear', 'rbf'), 'C': (1,4,8,16,32) }
svc = svm.SVC()
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(train_x_vectors, train_y)

from sklearn.metrics import f1_score

print("Exactitude")
print('Linear SVM\t', clf_svm.score(test_x_vectors, test_y))
print('Decision Tree\t', clf_dec.score(test_x_vectors, test_y))
print('Naive Bayes\t', clf_gnb.score(test_x_vectors.toarray(), test_y))
print('LogRegression\t', clf_log.score(test_x_vectors, test_y))
print('GridSearchCV\t', clf.score(test_x_vectors, test_y))

print()
print("F1")
print('Linear SVM\t', f1_score(test_y, clf_svm.predict(test_x_vectors), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('Decision Tree\t', f1_score(test_y, clf_dec.predict(test_x_vectors), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('Naive Bayes\t', f1_score(test_y, clf_gnb.predict(test_x_vectors.toarray()), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('LogRegression\t', f1_score(test_y, clf_log.predict(test_x_vectors), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('GridSearchCV\t', f1_score(test_y, clf.predict(test_x_vectors), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))

test_set = ['I am not happy with the work of this model, I think that it does not cope well with the definition of mood']
new_test = vectorized.transform(test_set)
clf_svm.predict(new_test)

test_set = ['A wonderful model, everything turned out exactly as I planned!!!']
new_test = vectorized.transform(test_set)
clf_svm.predict(new_test)

import pickle

# Сохранить модель в файл
# Enregistrer le modèle dans un fichier

with open('./sent_clf.pkl', 'wb') as f:
  pickle.dump(clf, f)

# Загрузить модель из файла
# Charger un modèle à partir d'un fichier

with open('./sent_clf.pkl', 'rb') as f:
  load_clf = pickle.load(f)