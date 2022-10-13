import base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2022))))

@st.cache
def load_data(year):                                            # функция загрузки дата-фрейма
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)                        # прочитать данные как html (таблицу)    
    print(html)                                                 # вывести данные в консоль 
    df = html[0]                                                # взять только первую колонку дата-сета 
    df['FG%'] = pd.to_numeric(df['FG%'], errors='coerce')       # конвертировать в число 
    df['eFG%'] = pd.to_numeric(df['eFG%'], errors='coerce')     # конвертировать в число  
    df['FT%'] = pd.to_numeric(df['FT%'], errors='coerce')       # конвертировать в число  
    df['3P%'] = pd.to_numeric(df['3P%'], errors='coerce')       # конвертировать в число 
    df['2P%'] = pd.to_numeric(df['2P%'], errors='coerce')       # конвертировать в число 
    raw = df.drop(df[df.Age == 'Age'].index)                    # удалить повторяющиеся заголовки
    raw = raw.fillna(0)                                         # пустые значения = 0 
    playerstats = raw.drop(['Rk'], axis=1)                      # удалить поле 'Rk' (создается автоматически)
    return playerstats                                          # вернуть дата-фрейм

# загрузить дата-сет с сайта (очищенный и готовый к выводу)
playerstats = load_data(selected_year)

# загрузить список команд
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# агрузить список позиций
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# выбрать из дата-сета выбранные данные
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')

# вывести данные как дата-сет
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

# скачать данные как CSV-файл
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
