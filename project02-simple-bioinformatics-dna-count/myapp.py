
import streamlit as st
import pandas as pd
import altair as alt

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.write("""
# DNA Nucleotide Count Web App

This App count the nucleotide composition of query DNA

***
""")

st.header('Enter DNA sequence')
sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"
sequence = st.text_area("Sequence input", sequence_input, height=150)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

st.write("""
***
""")

# st.header('INPUT (DNA Query)')
# sequence

st.header('OUTPUT (DNA Nucleotide Count)')

a1, a2 = st.columns(2)
b1, b2 = st.columns(2)

def DNA_nucleotide_count(seq):
    return dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])

with a1:
    st.subheader('1. Print as dictionary')
    X = DNA_nucleotide_count(sequence)
    X 

# X_label = list(X)
# X_values = list(X.X_values())

with a2:
    st.subheader('2. Print as text')
    st.write('There are ' + str(X['A']) + ' adenine (A)')
    st.write('There are ' + str(X['T']) + ' thymine (T)')
    st.write('There are ' + str(X['G']) + ' guanine (G)')
    st.write('There are ' + str(X['C']) + ' cytosine (C)')

with b1:
    st.subheader('3. Print as DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0:'count'}, axis='columns')
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'nucleotide'})
    st.write(df)

with b2:
    st.subheader('4. Print as Bar chart')
    p = alt.Chart(df).mark_bar().encode(x='nucleotide', y='count')
    p = p.properties(width=alt.Step(40))
    st.write(p)


