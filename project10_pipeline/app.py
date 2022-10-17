from pyspark.rdd import RDD
from pyspark.sql import Row
import streamlit as st
from utils import _initialize_spark

st.write("# :tada: Hello Pyspark")

spark, sc = _initialize_spark()
st.write("[Link to Spark window](http://localhost:4040)")

st.write("## Create RDD from a Python list")

l = list(range(10))
st.write(l)