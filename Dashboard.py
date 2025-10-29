import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as sc
from local_components import card_container

st.set_page_config(layout="wide", page_title='Cancer', page_icon=':bar_chart:')
st.title('Relación del Cancer')
st.markdown('##')

#Leer el archivo .csv
df=pd.read_csv('data/cancer-risk-factors.csv')
df.drop(['Patient_ID'], axis=1, inplace=True)
df.rename(columns={'Cancer_Type':'Tipo_de_Cancer', 'Age':'Edad','Gender':'Genero'}, inplace=True)
df['Tipo_de_Cancer']=df['Tipo_de_Cancer'].replace('Prostate','Prostata').replace('Skin','Piel').replace('Lung','Pulmon').replace('Breast','Seno') 
df['Genero']=df['Genero'].replace(0,'Femenino').replace(1,'Masculino') #Se cambio el 0 por femenino y el 1 por Masculino

#Desarrollar y/o escribir los filtros
columnas=st.columns(4) #Creo 3 columnas que funcionan como contenedor de los filtros
with columnas[0]:
    demografia=st.multiselect('Selecciones los aspectos demograficos a tener en cuenta:', options=df['Genero'].unique().tolist(), max_selections=1)
with columnas[1]:
    habitos=st.multiselect('Seleccione los habitos y Condiciones Ambientales a tener en cuenta:', options=df['Smoking'].unique().tolist(), default=df['Smoking'].unique().tolist())
with columnas[2]:
    historial_medico=st.multiselect('Seleccione el historial medico a tener en cuenta:', options=df['Family_History'].unique().tolist(), default=df['Family_History'].unique().tolist())
with columnas[3]:
    tipoc=st.multiselect('Seleccione el tipo de cancer:',options=df['Tipo_de_Cancer'].unique().tolist(), default=df['Tipo_de_Cancer'].unique().tolist())

#preguntar
data_filtered=df.loc[(df['Genero'].isin(demografia)) & (df['Smoking'].isin(habitos)) & (df['Family_History'].isin(historial_medico)) & (df['Tipo_de_Cancer'].isin(tipoc))]
'''
# ------ VISUALIZACIONES ------
st.subheader("Visualizaciones basadas en los filtros")

# Comprobar si el DataFrame filtrado no está vacío
if data_filtered.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
else:
    # Gráfico 1: Torta de Edad y Tipo de Cáncer (DISTRIBUCIÓN DEL TIPO DE CÁNCER)
    # Se recomienda mostrar la distribución del tipo de cáncer total, ya que la torta no es adecuada para dos variables.
    conteo_tipo_cancer = data_filtered.groupby('Tipo_de_Cancer').size().reset_index(name='Casos')
    fig1 = px.pie(conteo_tipo_cancer, values='Casos', names='Tipo_de_Cancer',
                  title='Distribución de Tipos de Cáncer')
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Historial Médico y Tipo de Cáncer (Gráfico de barras)
    fig2 = px.histogram(data_filtered, x='Family_History', color='Tipo_de_Cancer', barmode='group',
                       title='Casos de Cáncer según el Historial Familiar')
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Hábitos (Fumar) y Tipo de Cáncer (Gráfico de barras)
    fig3 = px.histogram(data_filtered, x='Smoking', color='Tipo_de_Cancer', barmode='group',
                       title='Casos de Cáncer según el Hábito de Fumar')
    st.plotly_chart(fig3, use_container_width=True)

    # Mostrar métricas adicionales
    st.markdown("### Métricas Clave")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Registros", value=len(data_filtered))
    with col2:
        st.metric(label="Casos de Cáncer Únicos", value=data_filtered['Tipo_de_Cancer'].nunique())
    with col3:
        st.metric(label="Edades Únicas", value=data_filtered['Edad'].nunique())'''