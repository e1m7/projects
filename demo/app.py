
import streamlit as st

# пример вывода текст
st.write("Hello World!")

# пример работы командной кнопки
if st.button('Say hello'):
    st.write('Why hello there')
    st.button('Why hello there')
else:
    st.write('Goodbye')
    st.button('Goodbye')