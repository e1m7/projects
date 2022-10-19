
import streamlit as st

st.write("""
# Créer un pipeline pour le DataSet "Cars"

Calculer pour chaque Fabricant (manufacturer_name)
1) nombre d'annonces
2) année de production moyenne de la machine
3) prix minimum
4) prix maximum
5) enregistrer le résultat dans output.csv

- [link](https://colab.research.google.com/drive/13IZZYmQ5mFQHZmvaXHqQsnaAss20OFF2?usp=sharing)
- [data](https://drive.google.com/file/d/1I1CCHUpHgDdObmRsrMlUD_rA36d-MA1g/view?usp=sharing)

***
""")

code = '''
# установить pyspark
# installer pyspark
!pip install pyspark

# импортировать функию для создания сессии
# importer une fonction pour créer une session
from pyspark.sql import SparkSession

# импортировать библиотеку дополнительных функций
# importer une bibliothèque de fonctionnalités avancées
import pyspark.sql.functions as F

# импортировать библиотеку конвертации типов данных
# importer la bibliothèque de conversion de type de données
import pyspark.sql.types as t

# загрузить файл с данными
# télécharger le fichier de données
from google.colab import files
files.upload()

# основная функция
# 1) создаем новую сессию
# 2) считываем дата-сет `cars.scv`, название колонок в первой строке
# 3) создаем дата-сет output (будет состоять из 5 колонок) 
# 4) он будет состоять из исходного дата-сета df
# 5) к которому применяем группировку по колонке `manufacturer_name` (индекс)
# 6) к которому применяем сложение данных для создания полей
# 7) число машин с таким именем в дата-сете = count("manufacturer_name")
# 8) средний год выпуска машин = округлить и перевести в `IntegerType` среднее число
# 9) минимальное значение в колонке `price_usd`
# 10) максимальное значение в колонке `price_usd`
# 11) сохранить файл result.csv на диске в 4 частях
# 12) показать ответ на экране

# fonction principale
# 1) créer une nouvelle session
# 2) nous lisons le datacet ' cars.scv`, nom des colonnes de la première ligne
# 3) créer un DateTime output (sera composé de 5 colonnes)
# 4) il sera composé du jeu de données DF d'origine
# 5) auquel nous appliquons le regroupement par la colonne 'manufacturer_name' (index)
# 6) à laquelle nous appliquons l'addition de données pour créer des champs
# 7) le nombre de machines portant ce nom dans le jeu de données = count ("manufacturer_name")
# 8) année de production moyenne des machines = arrondir et traduire en` IntegerType ' le nombre moyen
# 9) valeur minimale dans la colonne `price_usd`
# 10) valeur maximale dans la colonne `price_usd`
# 11) enregistrer le fichier result.csv sur le disque en 4 parties
# 12) afficher la réponse sur l'écran
def main():
  spark = SparkSession.builder.getOrCreate()
  df = spark.read.format("csv").option("header", "true").load("cars.csv")
  output = (
      df
        .groupBy("manufacturer_name")
        .agg(
            F.count("manufacturer_name").alias("count"),
            F.round(F.avg("year_produced")).cast(t.IntegerType()).alias("avg_year"),
            F.min(F.col("price_usd").cast(t.FloatType())).alias("min_price"),
            F.max(F.col("price_usd").cast(t.FloatType())).alias("max_price")
        )
  )
  output.coalesce(4).write.mode("overwrite").format("csv").save("result.csv")
  output.show()

main()

# +-----------------+-----+--------+---------+---------+
# |manufacturer_name|count|avg_year|min_price|max_price|
# +-----------------+-----+--------+---------+---------+
# |              Kia|  912|    2008|    200.0|  44700.0|
# |             LADA|  146|    2014|    120.0|  13800.0|
# |             Opel|  719|    2002|    200.0|  18190.0|
# |              УАЗ|   74|    1999|    379.4|  15000.0|
# |            Dodge|  297|    2003|    400.0|  35900.0|
# |           Subaru|  291|    2004|    400.0|  35500.0|
# +-----------------+-----+--------+---------+---------+
'''

st.code(code, language='python')