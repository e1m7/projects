
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

st.title("K-Nearest Neighbor")
cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, names=cols)

st.write("Afficher la date d'origine à l'écran")
st.dataframe(df.head(3))

df["class"] = (df["class"] == "g").astype(int)

st.write("Dans la Dernière colonne, remplacez les valeurs 'g| / 'h' par 0/1 afin que les modèles puissent les gérer facilement")
st.dataframe(df.head(3))

st.write("Nous déduisons pour 10 caractéristiques graphiques qui montrent comment la distribution de la Dernière colonne est liée (0,1)")
for label in cols[:-1]:
    a = df[df["class"]==1][label]
    b = df[df["class"]==0][label]
    x1 = np.random.uniform(0, 100, (1000))
    x2 = np.random.uniform(0, 100, (2000))
    x3 = np.random.uniform(0, 100, (3000))   
    hist_data = [x1, x2, x3]
    group_labels = ['Group1','Group2','Group3']
    figejemplo = ff.create_distplot(hist_data, group_labels, 
                             bin_size=[10, 10, 10, 10], show_hist=False, show_rug=False)
    st.plotly_chart(figejemplo, config=config, use_container_width=True)

    # arr = np.random.normal(1, 1, size=100)
    # fig, ax = plt.subplots()
    # ax.hist(a, bins=20)
    # st.pyplot(b)

#   plt.title(label)
#   plt.ylabel("Probability")
#   plt.xlabel(label)
#   plt.legend()
#   plt.show()
    # chart_data = pd.DataFrame(a, columns=b)
    # st.bar_chart(chart_data)