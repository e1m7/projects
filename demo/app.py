
import streamlit as st

# пример вывода текст
st.write("Hello World!")

def hello(a):
    st.write(f'All you need is love {a}')

# пример работы командной кнопки
if st.button('Say hello', help='Help self', on_click=hello, args=(1,2,3)):
    st.write('Why hello there')
else:
    st.write('Goodbye')