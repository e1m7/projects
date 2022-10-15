
import pandas as pd

# Прочитать очищенный дата-сет пингвинов
penguins = pd.read_csv('penguins_cleaned.csv')

# Подготавливаем данные для обработки
df = penguins.copy()
# Цель предсказания: вид пингвина
target = 'species'
# Характеристики: пол, остров
encode = ['sex', 'island']

# Создаем дата-сет для связывания вида, пола и острова
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy], axis=1)
    del df[col]

# Цели предсказания: три названия пингвинов
target_mapper = {
    'Adelie':0,
    'Chinstrap':1,
    'Gentoo':2
}

def target_encode(val):
    return target_mapper[val]

# Применяем фичи к челям предсказания
df['species'] = df['species'].apply(target_encode)

X = df.drop('species', axis=1)
Y = df['species']

# Строим модель случайного дерева
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X, Y)

import pickle
pickle.dump(clf, open('penguins_clf.pkl', 'wb'))
