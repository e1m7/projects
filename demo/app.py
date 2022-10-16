
import streamlit as st

# пример вывода текст
st.write("Hello World!")

def hello():
    st.write('All you need is love')

# пример работы командной кнопки
if st.button('Say hello', help='Help self', on_click=hello):
    st.write('Why hello there')
else:
    st.write('Goodbye')