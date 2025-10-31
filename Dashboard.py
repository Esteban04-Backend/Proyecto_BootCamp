import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as sc
from local_components import card_container

st.set_page_config(layout="wide", page_title='Cancer', page_icon=':bar_chart:')
st.title('Relación del Cancer')
st.markdown('##')

#Tratar los datos del .csv
df=pd.read_csv('data/cancer-risk-factors.csv')
#Se eliminan las columnas que no se van a usar para el dashboard
colum_eliminar=['Patient_ID','Overall_Risk_Score','Risk_Level']
df.drop(colum_eliminar, axis=1, inplace=True)
#Se renombra cada una de las columnas a Esapañol
df.rename(columns={'Cancer_Type':'Tipo_de_Cancer', 'Age':'Edad','Gender':'Genero','Smoking':'Tabaquismo(%)','Alcohol_Use':'Consumo_Alcohol(%)',
                   'Obesity':'Obesidad(%)','Family_History':'Antecedentes_Familiares','Diet_Red_Meat':'Dieta_Carnes_Rojas(%)',
                   'Diet_Salted_Processed':'Dieta_Salada_Procesada(%)','Fruit_Veg_Intake':'Consumo_Frutas_Verduras(%)',
                   'Physical_Activity':'Actividad_Fisica(%)','Air_Pollution':'Contaminacion_Atmosferica(%)','Occupational_Hazards':'Riesgos_Ocupacionales(%)',
                   'BRCA_Mutation':'Mutacion_BRCA','H_Pylori_Infection':'Infeccion_H_Pylori','Calcium_Intake':'Ingesta_Calcio(%)',
                   'BMI':'IMC','Physical_Activity_Level':'Nivel_Actividad_Fisica(%)'}, inplace=True)
#Se renombran los tipos de cancer por su traduccion en español
df['Tipo_de_Cancer']=df['Tipo_de_Cancer'].replace('Prostate','Prostata').replace('Skin','Piel').replace('Lung','Pulmon').replace('Breast','Seno') 
#Se ordenan los datos por la edad de los pacientes
df.sort_values(by='Edad',ascending=True, inplace=True)
#Se cambio el 0 y el 1 para cada tipo de columna:
#0=femenino 1=masculino
df['Genero']=df['Genero'].replace(0,'Femenino').replace(1,'Masculino')
#0 =negativo y 1 =Positivo"
df['Antecedentes_Familiares']=df['Antecedentes_Familiares'].replace(0,'Negativo').replace(1,'Positivo')
df['Mutacion_BRCA']=df['Mutacion_BRCA'].replace(0,'Negativo').replace(1,'Positivo')
df['Infeccion_H_Pylori']=df['Infeccion_H_Pylori'].replace(0,'Negativo').replace(1,'Positivo')
#Para las siguientes columnas se van a tratar sus datos en porcentaje para una mayor interpretacion
#Se selecciona un subconjunto de columnas a modificar y se realiza la operacion de multiplicar por 10 para sacar un porcentaje de 0% a 100%
columnas_procentaje=['Tabaquismo(%)','Consumo_Alcohol(%)','Obesidad(%)','Dieta_Carnes_Rojas(%)','Dieta_Salada_Procesada(%)','Consumo_Frutas_Verduras(%)',
                   'Actividad_Fisica(%)','Contaminacion_Atmosferica(%)','Riesgos_Ocupacionales(%)','Ingesta_Calcio(%)','Nivel_Actividad_Fisica(%)']
df[columnas_procentaje]=df[columnas_procentaje]*10
print('\nBase de datos Tratada')
print(df.head())

#Desarrollar y/o escribir los filtros
columnas=st.columns(4) #Creo 4 columnas que funcionan como contenedor de los filtros
with columnas[0]:
    tipoc=st.multiselect('Seleccione el tipo de cancer:',options=df['Tipo_de_Cancer'].unique().tolist(), max_selections=1)
with columnas[1]:
    demografia=st.multiselect('Selecciones los aspectos demograficos a tener en cuenta:', options=df['Genero'].unique().tolist(), default=df['Genero'].unique().tolist())
with columnas[2]:
    habitos=st.multiselect('Seleccione los habitos y Condiciones Ambientales a tener en cuenta:', options=df['Tabaquismo(%)'].unique().tolist(), default=df['Tabaquismo(%)'].unique().tolist())
with columnas[3]:
    historial_medico=st.multiselect('Seleccione el historial medico a tener en cuenta:', options=df['Antecedentes_Familiares'].unique().tolist(), default=df['Antecedentes_Familiares'].unique().tolist())


#preguntar
data_filtered=df.loc[(df['Genero'].isin(demografia)) & (df['Tabaquismo(%)'].isin(habitos)) & (df['Antecedentes_Familiares'].isin(historial_medico)) & (df['Tipo_de_Cancer'].isin(tipoc))]

# graficos

st.subheader("Visualizaciones basadas en los filtros")

# Comprobar si el DataFrame filtrado no está vacío
if data_filtered.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
else:
    # Gráfico 1: Torta de Edad y Tipo de Cáncer (DISTRIBUCIÓN DEL TIPO DE CÁNCER)
    conteo_tipo_cancer = data_filtered.groupby('Genero').size().reset_index(name='Casos')
    fig1 = px.pie(conteo_tipo_cancer, values='Casos', names='Genero',
                  title='Distribución de Tipos de Cáncer')
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Historial Médico y Tipo de Cáncer (Gráfico de barras)
    fig2 = px.histogram(data_filtered, x='Antecedentes_Familiares', color='Tipo_de_Cancer', barmode='group',
                       title='Casos de Cáncer según el Historial Familiar')
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Hábitos (Fumar) y Tipo de Cáncer (Gráfico de barras)
    fig3 = px.histogram(data_filtered, x='Tabaquismo(%)', color='Tipo_de_Cancer', barmode='group',
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
        st.metric(label="Edades Únicas", value=data_filtered['Edad'].nunique())