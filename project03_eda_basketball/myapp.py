
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer App')

st.markdown("""
This App performs simple webscraping of NBA player stats data
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
""")

# Создать левое меню приложения
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020 ))))

# Провести скраппинг данных
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)                              # прочитать html-данные за выбранынй год
    df = html[0]                                                    # создать дата-фрейм из таблицы
    raw = df.drop(df[df.Age == 'Age'].index)                        # удалить повторяющиеся года
    raw = raw.fillna(0)                                             # зполнить пропуски нулями
    playerstats = raw.drop(['Rk'], axis=1)                           # удалить столбец с индексами
    return playerstats                                               # вернуть дата-фрейм

# Получить данные за выбранный год
playerstats = load_data(selected_year)

# Вывести список команд (по алфавиту) и позволить выбирать их
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Вывести список позиций игроков и позволить выбирать их
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Фильтруем данные
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)

# Cкачать статистику игрока
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()        # строки в байты
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV-file</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Тепловая карта
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7,5)
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()