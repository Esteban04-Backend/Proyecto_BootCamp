import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit_shadcn_ui as sc
from local_components import card_container
#Configuracion del Dashboard 
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

#creacion de filtros teniendo en cuneta cada Columna
with st.sidebar:
    st.header('Filtros a Aplicar:')
#filtro para cada tipo de Cancer de solo una Selección
    tipoc=st.multiselect('Seleccione el tipo de cancer:',options=df['Tipo_de_Cancer'].unique().tolist(), max_selections=1)

    st.markdown('----')

    st.subheader('Aspectos Demograficos')
    genero=st.multiselect('Genero', 
                          options=df['Genero'].unique().tolist(), 
                          default=df['Genero'].unique().tolist())
    edad_min, edad_max = st.slider('Rango de Edad:',
                                   min_value=int(df['Edad'].min()),
                                   max_value=int(df['Edad'].max()),
                                   value=(int(df['Edad'].min()), int(df['Edad'].max())))
    IMC_min, IMC_max = st.slider('Rango de IMC:',
                                 min_value=float(df['IMC'].min()),
                                 max_value=float(df['IMC'].max()),
                                 value=(float(df['IMC'].min()), float(df['IMC'].max())))

    st.markdown('---')
#filtro para los habitos y condiciones ambientales de las personas
    st.subheader('Estilos de Vida y Aspectos Ambientales')
    taba_min, taba_max=st.slider('Porcentaje de Exposicion al Tabaco:',
                                 min_value=int(df['Tabaquismo(%)'].min()),
                                 max_value=int(df['Tabaquismo(%)'].max()),
                                 value=(int(df['Tabaquismo(%)'].min()), int(df['Tabaquismo(%)'].max())))
    alcoh_min, alcoh_max=st.slider('Porcentaje de Consumo de Alcohol:',
                                 min_value=int(df['Consumo_Alcohol(%)'].min()),
                                 max_value=int(df['Consumo_Alcohol(%)'].max()),
                                 value=(int(df['Consumo_Alcohol(%)'].min()), int(df['Consumo_Alcohol(%)'].max())))
    obes_min, obes_max=st.slider('Porcentaje de Obesidad:',
                                 min_value=int(df['Obesidad(%)'].min()),
                                 max_value=int(df['Obesidad(%)'].max()),
                                 value=(int(df['Obesidad(%)'].min()), int(df['Obesidad(%)'].max())))
    carn_min, carn_max=st.slider('Porcentaje de Ingesta de Carnes Rojas:',
                                 min_value=int(df['Dieta_Carnes_Rojas(%)'].min()),
                                 max_value=int(df['Dieta_Carnes_Rojas(%)'].max()),
                                 value=(int(df['Dieta_Carnes_Rojas(%)'].min()), int(df['Dieta_Carnes_Rojas(%)'].max())))
    salad_min, salad_max=st.slider('Porcentaje de Ingesta de Comida Salda Procesada:',
                                 min_value=int(df['Dieta_Salada_Procesada(%)'].min()),
                                 max_value=int(df['Dieta_Salada_Procesada(%)'].max()),
                                 value=(int(df['Dieta_Salada_Procesada(%)'].min()), int(df['Dieta_Salada_Procesada(%)'].max())))
    frut_min, frut_max=st.slider('Porcentaje de Ingesta de Frutas y Verduras:',
                                 min_value=int(df['Consumo_Frutas_Verduras(%)'].min()),
                                 max_value=int(df['Consumo_Frutas_Verduras(%)'].max()),
                                 value=(int(df['Consumo_Frutas_Verduras(%)'].min()), int(df['Consumo_Frutas_Verduras(%)'].max())))
    Nivef_min, Nivef_max=st.slider('Porcentaje del Nivel de Actividad Fisica Realizada:',
                                 min_value=int(df['Nivel_Actividad_Fisica(%)'].min()),
                                 max_value=int(df['Nivel_Actividad_Fisica(%)'].max()),
                                 value=(int(df['Nivel_Actividad_Fisica(%)'].min()), int(df['Nivel_Actividad_Fisica(%)'].max())))
    catm_min, catm_max=st.slider('Porcentaje de Exposición a la Contaminación Atmosferica:',
                                 min_value=int(df['Contaminacion_Atmosferica(%)'].min()),
                                 max_value=int(df['Contaminacion_Atmosferica(%)'].max()),
                                 value=(int(df['Contaminacion_Atmosferica(%)'].min()), int(df['Contaminacion_Atmosferica(%)'].max())))
    Roc_min, Roc_max=st.slider('Porcentaje de Riesgos Ocupacionales:',
                                 min_value=int(df['Riesgos_Ocupacionales(%)'].min()),
                                 max_value=int(df['Riesgos_Ocupacionales(%)'].max()),
                                 value=(int(df['Riesgos_Ocupacionales(%)'].min()), int(df['Riesgos_Ocupacionales(%)'].max())))
    igca_min, igca_max=st.slider('Porcentaje de Ingesta de Calcio:',
                                 min_value=int(df['Ingesta_Calcio(%)'].min()),
                                 max_value=int(df['Ingesta_Calcio(%)'].max()),
                                 value=(int(df['Ingesta_Calcio(%)'].min()), int(df['Ingesta_Calcio(%)'].max())))
    st.markdown('---')
#filtro para los Indicadores geneticos y medicos
    st.subheader('Indicadores Genéticos y Médicos')
    antf=st.multiselect('Antecedentes_Familiares', options=df['Antecedentes_Familiares'].unique().tolist(),default=df['Antecedentes_Familiares'].unique().tolist())
    mutacion=st.multiselect('Mutacion_BRCA', options=df['Mutacion_BRCA'].unique().tolist(),default=df['Mutacion_BRCA'].unique().tolist())
    infecHpylori=st.multiselect('Infeccion_H_Pylori', options=df['Infeccion_H_Pylori'].unique().tolist(),default=df['Infeccion_H_Pylori'].unique().tolist())

#Se crea una copia del data frame para no modificar el original cuando se apliquen los diferentes filtros
df_seleccion=df.copy()
df_seleccion=df_seleccion[df_seleccion['Genero'].isin(genero)]
#Para evitar posibles errores en la seleccion de tipo de cancer si el  usuario no selecciona ninguna
if tipoc:
    df_seleccion=df_seleccion[df_seleccion['Tipo_de_Cancer'].isin(tipoc)]

#Aplicamos la copia del df para cada uno de los rangos definidos asi no modificamos el da original
df_seleccion = df_seleccion[
    (df_seleccion['Edad'] >= edad_min) & (df_seleccion['Edad'] <= edad_max) &
    (df_seleccion['IMC'] >= IMC_min) & (df_seleccion['IMC'] <= IMC_max) &
    (df_seleccion['Tabaquismo(%)'] >= taba_min) & (df_seleccion['Tabaquismo(%)'] <= taba_max) &
    (df_seleccion['Consumo_Alcohol(%)'] >= alcoh_min) & (df_seleccion['Consumo_Alcohol(%)'] <= alcoh_max) &
    (df_seleccion['Obesidad(%)'] >= obes_min) & (df_seleccion['Obesidad(%)'] <= obes_max) &
    (df_seleccion['Dieta_Carnes_Rojas(%)'] >= carn_min) & (df_seleccion['Dieta_Carnes_Rojas(%)'] <= carn_max) &
    (df_seleccion['Dieta_Salada_Procesada(%)'] >= salad_min) & (df_seleccion['Dieta_Salada_Procesada(%)'] <= salad_max) &
    (df_seleccion['Consumo_Frutas_Verduras(%)'] >= frut_min) & (df_seleccion['Consumo_Frutas_Verduras(%)'] <= frut_max) &
    (df_seleccion['Nivel_Actividad_Fisica(%)'] >= Nivef_min) & (df_seleccion['Nivel_Actividad_Fisica(%)'] <= Nivef_max) &
    (df_seleccion['Contaminacion_Atmosferica(%)'] >= catm_min) & (df_seleccion['Contaminacion_Atmosferica(%)'] <= catm_max) &
    (df_seleccion['Riesgos_Ocupacionales(%)'] >= Roc_min) & (df_seleccion['Riesgos_Ocupacionales(%)'] <= Roc_max) &
    (df_seleccion['Ingesta_Calcio(%)'] >= igca_min) & (df_seleccion['Ingesta_Calcio(%)'] <= igca_max)]
# Aplicar filtros de selección múltiple para Antecedentes y Mutaciones
df_seleccion = df_seleccion[df_seleccion['Antecedentes_Familiares'].isin(antf)]
df_seleccion = df_seleccion[df_seleccion['Mutacion_BRCA'].isin(mutacion)]
df_seleccion = df_seleccion[df_seleccion['Infeccion_H_Pylori'].isin(infecHpylori)]

#Prueba de Grafico

# --- Inicio de la implementación de Visualizaciones ---

# Manejo de dataframe vacío si no hay datos tras los filtros
if df_seleccion.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
    st.stop()

# 1. Vista Macro/General de los Datos

st.markdown('### Análisis General de la Población')

# Calcular métricas clave para las tarjetas
total_pacientes = len(df_seleccion)
promedio_edad = round(df_seleccion['Edad'].mean(), 1)
genero_mas_comun = df_seleccion['Genero'].mode()[0] if not df_seleccion['Genero'].empty else 'N/A'

# Mostrar métricas usando streamlit_shadcn_ui cards
col_metric1, col_metric2, col_metric3 = st.columns(3)

with col_metric1:
    sc.card(title="Total Pacientes", content=f"{total_pacientes}", description="Registros filtrados", key="card1")
with col_metric2:
    sc.card(title="Edad Promedio", content=f"{promedio_edad} años", description="Media de edad", key="card2")
with col_metric3:
    sc.card(title="Género Más Común", content=f"{genero_mas_comun}", description="Moda del género", key="card3")

st.markdown('##') # Espaciado

col_macro1, col_macro2 = st.columns([2, 1])

with col_macro1:
    st.subheader('Distribución de Tipos de Cáncer')
    # Gráfico de Rectángulos (Treemap) para visualizar proporciones
    fig_treemap = px.treemap(
        df_seleccion,
        path=['Tipo_de_Cancer', 'Genero'],
        title='Proporción de Tipos de Cáncer y Género',
        color='Tipo_de_Cancer'
    )
    fig_treemap.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig_treemap, use_container_width=True)

with col_macro2:
    st.subheader('Distribución por Género')
    # Gráfico Circular para mostrar la proporción de género
    fig_pie_gender = px.pie(
        df_seleccion,
        names='Genero',
        title='Distribución de Pacientes por Género',
        hole=0.3 # Gráfico de dona
    )
    st.plotly_chart(fig_pie_gender, use_container_width=True)


# 2. Vista Intermedia: Relaciones Demográficas y Genéticas

st.markdown('---')
st.markdown('### Análisis Demográfico y Factores Genéticos/Médicos')

col_intermedia1, col_intermedia2 = st.columns(2)

with col_intermedia1:
    st.subheader('Histograma de Edad por Género')
    # Histograma agrupado para la edad
    fig_hist_age = px.histogram(
        df_seleccion,
        x='Edad',
        color='Genero',
        marginal="box", # Añade un box plot marginal para mejor análisis
        nbins=20,
        title='Distribución de Edad Agrupada por Género'
    )
    st.plotly_chart(fig_hist_age, use_container_width=True)

with col_intermedia2:
    st.subheader('Frecuencia de Factores Genéticos/Médicos')
    # Gráfico de barras para factores categóricos (ejemplo con Antecedentes)
    # Se puede expandir para incluir Mutacion_BRCA e Infeccion_H_Pylori
    df_genetics = df_seleccion.melt(value_vars=['Antecedentes_Familiares', 'Mutacion_BRCA', 'Infeccion_H_Pylori'],
                                    var_name='Factor', value_name='Estado')
    fig_bar_genetics = px.histogram(
        df_genetics,
        x='Factor',
        color='Estado',
        barmode='group',
        title='Comparación de Indicadores Genéticos y Médicos'
    )
    st.plotly_chart(fig_bar_genetics, use_container_width=True)


# 3. Vista Micro/Detalle: Análisis de Hábitos y Factores Cuantitativos

# --- Sección 3. Análisis Detallado (Micro): Hábitos y Factores Cuantitativos ---

st.header("Análisis Detallado (Micro): Hábitos y Factores Cuantitativos")

# Definición de las columnas porcentuales (asegúrate de que esta lista esté definida en tu código principal)
columnas_procentaje = ['Tabaquismo(%)','Consumo_Alcohol(%)','Obesidad(%)','Dieta_Carnes_Rojas(%)','Dieta_Salada_Procesada(%)','Consumo_Frutas_Verduras(%)',
                   'Actividad_Fisica(%)','Contaminacion_Atmosferica(%)','Riesgos_Ocupacionales(%)','Ingesta_Calcio(%)','Nivel_Actividad_Fisica(%)']

# 3a. Vista General de Hábitos (Macro de los Micro)
st.subheader("Nivel Promedio de Exposición a Factores de Riesgo (Gráfico de Líneas/Puntos)")

# Usamos melt para apilar los porcentajes y luego calculamos la media global para cada factor.
df_habitos_melt_avg = df_seleccion[columnas_procentaje].melt(var_name='Factor de Riesgo', value_name='Nivel Porcentual')

# Calcular el promedio de cada factor
df_avg_scores = df_habitos_melt_avg.groupby('Factor de Riesgo')['Nivel Porcentual'].mean().reset_index()

# Gráfico de líneas con puntos grandes (Eje X: Factores, Eje Y: Promedio)
fig_avg_factors = px.line(
    df_avg_scores,
    x='Factor de Riesgo',
    y='Nivel Porcentual',
    title="Nivel Promedio Global de Exposición a Factores de Riesgo",
    markers=True
)
fig_avg_factors.update_traces(line=dict(color='gray', width=1)) 
fig_avg_factors.update_traces(marker=dict(size=12, color='blue'))
fig_avg_factors.update_layout(xaxis_tickangle=-45, yaxis_title="Nivel Porcentual Promedio (%)")
st.plotly_chart(fig_avg_factors, use_container_width=True)

st.markdown('---')

# 3b. Vista Detallada de Hábitos (Micro de los Micro)

st.subheader("Análisis de Dispersión y Distribución Detallado")

# Dropdown para seleccionar qué factor de riesgo analizar con detalle
factor_detalle_micro = st.selectbox(
    'Seleccione el factor de riesgo a analizar detalladamente su dispersión:',
    options=columnas_procentaje
)

col_micro1, col_micro2 = st.columns(2)

with col_micro1:
    st.markdown(f'##### Distribución de "{factor_detalle_micro}" (Polígono de Frecuencias Manual)')
    
    fig_poly = go.Figure()
    
    for genero_val in df_seleccion['Genero'].unique():
        df_sub = df_seleccion[df_seleccion['Genero'] == genero_val].dropna(subset=[factor_detalle_micro, 'Edad'])
        if not df_sub.empty:
            hist_data, edges = np.histogram(df_sub[factor_detalle_micro], bins=20, density=True)
            centers = [(edges[i] + edges[i+1]) / 2 for i in range(len(edges) - 1)]
            
            fig_poly.add_trace(
                go.Scatter(
                    x=centers, 
                    y=hist_data, 
                    mode='lines+markers', 
                    name=f'{genero_val}',
                    line=dict(width=2.5, shape='spline'),
                    marker=dict(size=5)
                )
            )
        
    fig_poly.update_layout(
        title=f'Polígono de Frecuencias para {factor_detalle_micro} por Género',
        xaxis_title=factor_detalle_micro,
        yaxis_title="Densidad de Frecuencia"
    )
    st.plotly_chart(fig_poly, use_container_width=True)


with col_micro2:
    st.markdown(f'##### Relación entre {factor_detalle_micro} y Edad (Dispersión)')
    
    # Preparamos una copia limpia del dataframe SOLO para este gráfico para asegurar que OLS funcione
    df_scatter_clean = df_seleccion.dropna(subset=['Edad', factor_detalle_micro, 'Genero'])
    
# Verificamos si hay suficientes datos para la línea de tendencia después de limpiar
    with col_micro2:
        st.markdown(f'##### Relación entre {factor_detalle_micro} y Edad (Dispersión)')
    
    # ... código de limpieza de datos ...

    fig_scatter = px.scatter(
        df_scatter_clean,
        x='Edad',  # <-- Eje X: Edad
        y=factor_detalle_micro, # <-- Eje Y: El factor porcentual seleccionado
        color='Genero',
        trendline='ols',
        title=f'Relación entre Edad y {factor_detalle_micro}',
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
print('Vamos bien')