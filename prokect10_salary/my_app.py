
import streamlit as st

st.write("""
# Prévision du salaire des employés

Étant donné un ensemble de données simple avec des champs : nom, âge, expérience, 
salaire de l'employé. Créer un modèle qui, compte tenu de **l'âge** et de **l'expérience**, 
prédit la valeur **salariale** d'un employé

- [link](https://colab.research.google.com/drive/1k3_KMTVcWO0kPbLFR8--N1AX1Kuh7KMM?usp=sharing)
- [data](https://drive.google.com/file/d/1WpLIbsVZu_47CwSOBJcjMt0cHqNbVWbR/view?usp=sharing)

***
""")

code = '''
# установить pyspark
# installer payspark
!pip install pyspark

# импортировать pyspark
# importer payspark
import pyspark

# импортировать pandas
# importer pandas
import pandas as pd

# импортировать SparkSession
# importer SparkSession
from pyspark.sql import SparkSession

# создать новый сеан Spark с названием "Практика"
# créer une nouvelle session Spark nommée "Pratique"
spark = SparkSession.builder.appName('Practic').getOrCreate()
spark

# импортировать функцию для считывания файла
# importer la fonction pour lire le fichier
from google.colab import files

# загрузить файл
# télécharger le fichier
uploaded = files.upload()

# считать файл с диска, названия колонок в первой строке, учитывать схему
# lire le fichier à partir du disque, les noms des colonnes dans la première ligne, prendre en compte le schéma
df = spark.read.csv('salary.csv', header=True, inferSchema=True)

# вывести датасет, названия колонок, типы колонок и схему
# afficher le DataSet, les noms des colonnes, les types de colonnes et le schéma
df.show()
df.columns
df.dtypes
df.printSchema()

# +---------+---+----------+------+
# |     Name|age|Experience|Salary|
# +---------+---+----------+------+
# |    Krish| 31|        10| 30000|
# |Sudhanshu| 30|         8| 25000|
# |    Sunny| 29|         4| 20000|
# |     Paul| 24|         3| 20000|
# |   Harsha| 21|         1| 15000|
# |  Shubham| 23|         2| 18000|
# +---------+---+----------+------+

# подключаем вектор ассемблирования (сбор фичей в одну колонку)
# nous connectons le vecteur d'assemblage (collection de figures dans une colonne)
from pyspark.ml.feature import VectorAssembler

# собираем данные из `возраст` и `опыт работы` в одну колонку `независимые фичи`
# recueillir des données de ' âge ' et 'expérience' dans une colonne ' caractéristiques indépendantes`
featureassembler = VectorAssembler(inputCols=["age","Experience"], outputCol="Independent Features")

# добавляем новую колонку к основному датасету
# nous ajoutons une nouvelle colonne au DataSet principal
output = featureassembler.transform(df)

# выбираем две колонки: новая и зарплата (финальный набор данных)
# choisissez deux colonnes: nouveau et salaire (jeu de données final)
final_data = output.select("Independent Features", "Salary")

# подключаем библиотеку для обработки линейной регрессии
# nous connectons la bibliothèque pour le traitement de la régression linéaire
from pyspark.ml.regression import LinearRegression

# разбиваем финальный набор на тренировочный и тестовый (75/25)
# nous divisons l'ensemble final en formation et test (75/25)
train_data, test_data = final_data.randomSplit([0.75, 0.25])

# создаем регрессионную модель данных
# créer un modèle de régression de données
regressor = LinearRegression(featuresCol="Independent Features", labelCol="Salary")

# обучаем модель
# former le modèle
regressor = regressor.fit(train_data)

# выводим найденные коэффициенты
# nous affichons les coefficients trouvés
regressor.coefficients

# выводим перехват (смещение)
# sortie interception (offset)
regressor.intercept

# сделать предсказание для тестового набора данных
# faire une prédiction pour l'ensemble de données de test
pred_results = regressor.evaluate(test_data)

# показать предсказание и реальную зарплату тестового набора
# afficher la prédiction et le salaire réel de l'ensemble de test
pred_results.predictions.show()

# показать абсолютную ошибку, квадратичную ошибку
# afficher l'erreur absolue, l'erreur quadratique
pred_results.meanAbsoluteError, pred_results.meanSquaredError

# +--------------------+------+------------------+
# |Independent Features|Salary|        prediction|
# +--------------------+------+------------------+
# |          [21.0,1.0]| 15000|16035.087719298195|
# |          [29.0,4.0]| 20000| 24140.35087719302|
# |          [30.0,8.0]| 25000| 27824.56140350881|
# +--------------------+------+------------------+

# (2666.6666666666756, 8730686.365035541)
'''

st.code(code, language='python')