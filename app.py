import streamlit as st
import pandas as pd
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Titre et sous-titre
st.title("Atelier StreamLit - Docker - Heroku - GitHub Actions M2 SISE")
st.subheader("Exploration des données des résultats des étudiants de deux écoles portuguaise")

uploaded_file = st.file_uploader("Chargement du fichier")
                 
@st.cache(persist=True)     
def upload(uploaded_file):
    dataframe = pd.read_csv(uploaded_file, sep = ';')
    return dataframe


def histchart(df):  
    result = df.groupby(['school','reason']).size().reset_index(name='counts')
    fig = px.bar(result, x='school', y='counts', color='reason', height=400)
    return fig


def piechart(df):       
    resultM = df.groupby(['Mjob']).size().reset_index(name='counts')
    resultF = df.groupby(['Fjob']).size().reset_index(name='counts')   
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=resultM.Mjob, values=resultM.counts, name="Mère"),
                  1, 1)
    fig.add_trace(go.Pie(labels=resultF.Fjob, values=resultF.counts, name="Père"),
                  1, 2)  
    
    fig.update_layout(
        title_text="Profession des parents")
    return fig


def boxplot(df):       
    categories_count = ['G1', 'G2', 'G3']
    chosen_count = st.selectbox(
       'Quel trimestre ?', categories_count)
    fig = px.box(df, x='studytime', y=chosen_count, color='schoolsup', notched=True)
    return fig
 

if uploaded_file is not None:
    data = upload(uploaded_file)
    genre = st.sidebar.radio(
             "Genre",
            ('Tout', 'Homme', 'Femme'))
    if genre == 'Femme':
        data = data.loc[data['sex']=='F',:]
    elif genre == 'Homme':
        data = data.loc[data['sex']=='M',:]  

    sorti = st.sidebar.radio(
             "Temps passé avec les amis",
            ('Aucun', 'Très peu', 'Peu','Moyennement','Souvent','Très souvent'))
    if sorti == 'Très peu':
        data = data.loc[data['goout']==1,:]
    elif sorti == 'Peu':
        data = data.loc[data['goout']==2,:]
    elif sorti == 'Moyennement':
        data = data.loc[data['goout']==3,:]
    elif sorti == 'Souvent':
        data = data.loc[data['goout']==4,:]
    elif sorti == 'Très souvent':
        data = data.loc[data['goout']==5,:]

    st.write(data)
    hist = histchart(data)
    st.write(hist)
    pie = piechart(data)
    st.write(pie)
    boxplot = boxplot(data)
    st.plotly_chart(boxplot)
    