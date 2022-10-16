
import streamlit as st
from datetime import date
import yfinance as yf
from fbprphet import Prophet
from fbprphet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stocl Prediction App')

stocks = ('AAPL','GOOG','MSFT')
selected_stocks = st.selectbox("Select dataset for prediction", stocks)
n_years = st.slider("Years of prediction", 1, 4)
period = n_years * 365
