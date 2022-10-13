import streamlit as st
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

url = "https://www.basketball-reference.com/playoffs/"
html = urlopen(url)
soup = BeautifulSoup(html, features="lxml")
headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
rows = soup.findAll('tr')[2:]
rows_data = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
rows_data.pop(20)
rows_data = rows_data[0:38]
last_year = 2020
for i in range(0, len(rows_data)):
    rows_data[i].insert(0, last_year)
    last_year -=1

nba_finals = pd.DataFrame(rows_data, columns=headers)
answer = nba_finals.loc[nba_finals['Year'] == selected_year]
st.write(answer)

