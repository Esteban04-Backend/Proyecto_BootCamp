import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


#Configuracion del Dashboard 
st.set_page_config(layout="wide", page_title='Cancer', page_icon=':bar_chart:')
st.title('Relación del Cancer')
st.markdown('##')

#Tratar los datos del .csv
df=pd.read_csv('data/cancer-risk-factors.csv')
#Se eliminan las columnas que no se van a usar para el dashboard
colum_eliminar=['Patient_ID','Overall_Risk_Score','Risk_Level']
df.drop(colum_eliminar, axis=1, inplace=True)
#Se renombra cada una de las columnas a Español
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
    st.subheader('Estilos de Vida y Aspectos Ambientales')#el sub.header me ayuda a crear un titulo de la seccion 
    taba_min, taba_max=st.slider('Porcentaje de Exposicion al Tabaco:', #se hace una barra slider ya continuación va el titulo del slider que nos permite seleccionar un rango de valores
                                 min_value=int(df['Tabaquismo(%)'].min()), #establecemos el valor minimo del slider  y lo convertimos a entero
                                 max_value=int(df['Tabaquismo(%)'].max()), #establecemos el valor maximo del slider y lo convertimos a entero
                                 value=(int(df['Tabaquismo(%)'].min()), int(df['Tabaquismo(%)'].max()))) #creamos una variable que almacena el valor minimo y maximo de la columna selecciona y los trae 
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
    st.markdown('---') #con el markdown se inserta una linea horizontal que separa una cosa de otra
#filtro para los Indicadores geneticos y medicos
    st.subheader('Indicadores Genéticos y Médicos') #crea otro subtitulo de la barra lateral
    antf=st.multiselect('Antecedentes_Familiares', options=df['Antecedentes_Familiares'].unique().tolist(),default=df['Antecedentes_Familiares'].unique().tolist()) #el multiselect nos crea un cajon de seleccion multiple
    #la funcion unique trae los datos unicos de la columna que especificamos y el tolist lo convierte en una lista  y el default establece por defecto todas las opciones seleccionadas al cargar la pagina
    mutacion=st.multiselect('Mutacion_BRCA', options=df['Mutacion_BRCA'].unique().tolist(),default=df['Mutacion_BRCA'].unique().tolist())
    infecHpylori=st.multiselect('Infeccion_H_Pylori', options=df['Infeccion_H_Pylori'].unique().tolist(),default=df['Infeccion_H_Pylori'].unique().tolist())

#Se crea una copia del data frame para no modificar el original cuando se apliquen los diferentes filtros
df_seleccion=df.copy()
df_seleccion=df_seleccion[df_seleccion['Genero'].isin(genero)] # filtramos el df_selec por la columna genero y el isin verifica que los elementos si estan contenidos en una secuencia de valores principalmente en la lista genero
#Para evitar posibles errores en la seleccion de tipo de cancer si el  usuario no selecciona ninguna
if tipoc: #se realiza una comrpobacion condicional y solo se ejecutara para el tipo de cancer (tipoc)
    df_seleccion=df_seleccion[df_seleccion['Tipo_de_Cancer'].isin(tipoc)] #filtra y mantiene solo las filas donde el valor de la columna tipo de cancer esta en la lista tipoc

#Aplicamos la copia del df para cada uno de los rangos definidos asi no modificamos el da original
df_seleccion = df_seleccion[
    (df_seleccion['Edad'] >= edad_min) & (df_seleccion['Edad'] <= edad_max) &
    # con edad_min compara cada valor de la columna edad con el valor de la variable edad_min  y me devuelve un True si Edad es mayor o igual que edad min y false si es menor que edad min
    # con edad_max compara cada valor de la columna edad con el valor de la variable edad_max  y me devuelve un True si Edad es menor o igual que edad max y false si es mayor que edad max
    #el operador  & combina ambas condiciones y devuelve true si ambas condiciones son verdades por tal razon solo se mantiene lsa filas para que el filtro es verdadero
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
if df_seleccion.empty: #para verificar si el df esta vacio se usa el .empty 
    st.warning("No hay datos que coincidan con los filtros seleccionados.") # muestra un aviso de advertencia (.warning)
    st.stop() #lo que hace es detener la ejecucion del resto del script de python para que no se generen errores 

#Vista General de los Datos de la población

st.markdown('## _Análisis General de la Población_') ##markdown insertar texto (##=susbtitulo, _texto_=cursiva)

# Calcular métricas clave para las tarjetas
total_pacientes = len(df_seleccion) #cuenta el total de pacientes en el df seleccion (el df que se usa para los filtros)
promedio_edad = round(df_seleccion['Edad'].mean(), 0) #.mean se usa para calcular el promedio de la columna edad, y se redondea con el round a 1 decimal
genero_mas_comun = df_seleccion['Genero'].mode()[0] if not df_seleccion['Genero'].empty else 'N/A' #.mode se usa para encontrar los valores que aparecen con mas frecuencia osea es la moda de la columna seleccionada el 0 me devuelve solo el primer valos de la moda ( si hay 2 modas solo me devuelve el primero)
#Calcula el género más común y guárdalo. Pero si no hay datos para calcularlo, simplemente escribe 'N/A' para evitar un error en mi programa.

# Mostrar métricas usando streamlit metric
col_metric1, col_metric2, col_metric3 = st.columns(3)#. columns me crea 3 sepraciones horizontales tipo columnas
with col_metric1: #todo dentro de with se debe de colocar dentre de la columna nombrada a continuación
    st.metric(label="Total Pacientes", value=f"{total_pacientes}", delta="Registros filtrados") #.metric me muestra las columnas con los datos filtrados de manera independiente. 
with col_metric2:
    st.metric(label="Edad Promedio", value=f"{promedio_edad} años", delta="Media de edad")
with col_metric3:
    st.metric(label="Género Más Común", value=f"{genero_mas_comun}", delta="Moda del género")

st.markdown('##') # Espacios entre el 1 y el siguiente subtitulo

col_macro1, col_macro2 = st.columns([2, 1]) #el 2,1 se hace para tener en cuenta la relacion de cada uno de las columnas osea el ancho


st.subheader('**_Distribución de Tipos de Cáncer_**')
    # Gráfico de Rectángulos (Treemap) para visualizar proporciones de cada uno de los tipos de cancer
fig_treemap = px.treemap(
    df_seleccion,
    path=['Tipo_de_Cancer','Genero'],
    title='Proporción de Tipos de Cáncer y Género',
    color='Tipo_de_Cancer', color_discrete_sequence=px.colors.qualitative.Pastel)
fig_treemap.update_traces(textinfo="label+percent parent")#el textinfo lo que hace e que me muestra como la etiqueta (masculino, femenino) 
#y el percent muestra el porcentaje en relacion a esa parte de la etiqueta que cumple con el tipo de cancer
st.plotly_chart(fig_treemap, use_container_width=True)#fig:lo usamos para que lo grafique en el navegador y el use es para ajustar automaticamente el ancho
col_macro1, col_macro2 = st.columns(2) #el 2,1 se hace para tener en cuenta la relacion de cada uno de las columnas osea el ancho
color_genero={'Femenino':'#FF00FF','Masculino':'#007BFF'}

with col_macro1:
    st.subheader('**_Distribución por Género_**')
    # Gráfico Circular y / o torta para mostrar la proporción de género
    fig_pie_gender = px.pie(
        df_seleccion,
        names='Genero',
        title='Distribución de Pacientes por Género',
        hole=0.3, # Circulo interior del procentaje
        color='Genero',color_discrete_map=color_genero)
    st.plotly_chart(fig_pie_gender, use_container_width=True)

with col_macro2:
    st.subheader('Distribución de Edad Agrupada por Género')
    # Histograma agrupado para la edad
    histo_edad = px.histogram(
        df_seleccion,
        x='Edad',
        color='Genero',color_discrete_map=color_genero,
        nbins=20,
        barmode='group', 
        #opacity=0.6,
        #text_auto=True,
        labels={'count':'Cantidad de Personas'})
    histo_edad.update_xaxes(dtick=5)
    histo_edad.update_traces(marker_line_width=0.1, marker_line_color="black")
    histo_edad.update_yaxes(title_text='Cantidad de Personas')
    st.plotly_chart(histo_edad, use_container_width=True)
# 2. Vista Intermedia: Relaciones Demográficas y Genéticas

st.markdown('---')
st.markdown('### Análisis de Factores Genéticos y Médicos')

col_intermedia1, col_intermedia2 = st.columns([1,2])

color_negypos={'Negativo':'#007BFF','Positivo':'#DC3545'}
with col_intermedia1:
    st.subheader('Incidencia Individual de Indicadores Genéticos y Médicos')
    # Gráfico de barras para factores categóricos (ejemplo con Antecedentes)
    df_geneticos = df_seleccion.melt(value_vars=['Antecedentes_Familiares', 'Mutacion_BRCA', 'Infeccion_H_Pylori'],
                                    var_name='Factor', value_name='Estado') #.melt me hace una agrupacion para despues contarlos y graficarlos
    bar_geneticos = px.histogram(
        df_geneticos,
        x='Factor',
        color='Estado',color_discrete_map=color_negypos,
        text_auto=True,
        barmode='group')
    bar_geneticos.update_traces(marker_line_width=1, marker_line_color="black")
    bar_geneticos.update_yaxes(title_text='Cantidad de Personas')
    st.plotly_chart(bar_geneticos, use_container_width=True)

with col_intermedia2:
    #Agrupar por las 3 columnas para contar la frecuencia exacta de cada combinación
    st.subheader('Análisis de Coexistencia de Indicadores Genéticos y Médicos')
    st.markdown('##')
    df_conteo_combinado = df_seleccion.groupby([
        'Antecedentes_Familiares', 
        'Mutacion_BRCA', 
        'Infeccion_H_Pylori'
    ]).size().reset_index(name='Cantidad de Pacientes')

    #Mostrar la tabla en Streamlit, ocultando el índice
    st.dataframe(df_conteo_combinado,use_container_width=True, hide_index=True) # <-- Esto oculta la primera columna numérica (el índice))

# 3. Vista Micro/Detalle: Análisis de Hábitos y Factores Cuantitativos
# Definición de las columnas porcentuales (asegúrate de que esta lista esté definida en tu código principal)
columnas_procentaje = ['Tabaquismo(%)','Consumo_Alcohol(%)','Obesidad(%)','Dieta_Carnes_Rojas(%)','Dieta_Salada_Procesada(%)','Consumo_Frutas_Verduras(%)',
                   'Contaminacion_Atmosferica(%)','Riesgos_Ocupacionales(%)','Ingesta_Calcio(%)','Nivel_Actividad_Fisica(%)']

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
fig_avg_factors.update_traces(marker=dict(size=12, color='Red'))
fig_avg_factors.update_layout(xaxis_tickangle=-45, yaxis_title="Nivel Porcentual Promedio (%)")
st.plotly_chart(fig_avg_factors, use_container_width=True)

st.markdown('---')

#Vista Detallada de los Hábitos

st.subheader("Análisis de Dispersión y Distribución Detallado")

# Dropdown para seleccionar qué factor de riesgo analizar con detalle
factor_detalle_micro = st.selectbox( #selectbox me ayuda a crear un menu desplegable en la pagina web
    'Seleccione el factor de riesgo a analizar detalladamente su dispersión:',
    options=columnas_procentaje) #Limita al usuario que opciones puede elegir

col_micro1, col_micro2 = st.columns(2)

with col_micro1:
    st.markdown(f'### Distribución de Pacientes por género para {factor_detalle_micro}')
    
    #A continuacion se realiza una agrupacion de los datos. 
    df_agrupado = df_seleccion.groupby([factor_detalle_micro, 'Genero']).size().reset_index(name='Cantidad')#creamos un nuevo dataframe para poderlas agrupar por dos columnas la ctageoria que es dinamica y el genero
    #el .size me ayuda a contar el numero de columnas de los grupos creados y el .reset_index me asigna un nuevo nombre a la columna creada con el size
    
    fig = go.Figure() #creamos una figura vacia en la que mas adelante vamos a añadir graficos de linea columna etc.
    
    # a continuacion se crea un ciclo para poder generar por cada género una barras
    for genero in df_agrupado['Genero'].unique(): #iniciamos un bucle que va a recorrer cada uno de los valores unicos de la columna genero
        df_gen = df_agrupado[df_agrupado['Genero'] == genero] #creamos una copia del df para filtrarlas solo por las filas que coincidan con el genero
        
        fig.add_trace(go.Bar( #se agrega un trazo con el add_trace pero para este caso especificamente se agrega un grafico de barras con go.bar
            x=df_gen[factor_detalle_micro],#establecemos los valores del eje x
            y=df_gen['Cantidad'],#damos los valores para el eje y
            name=genero, #se asigna el nombre para las barras creadas
            marker_color=color_genero[genero], # asigna el color para las barras por cada genero
            marker_line_width=1, marker_line_color="black", #definimos el estilo del borde de las barras ancho y color
            text=df_gen['Cantidad'].astype(int), #mostramos la cantidad dentro de la barra y el .asytype nos asegura que el numero sea entero
            textposition='inside')) #nos ayuda a colorcar la cantudad en el centro de la barra

    #Configuramos el diseño, distribuacion y las anotaciones para el total
    fig.update_layout( #con el .update actualiazmos la configuracion general del diseño
        barmode='stack', legend_title_text='Género', #el stack aplia las columnas una sobre otra y el legend etsablece el titulo de las leyendas del grafico
        yaxis_title_text='Cantidad de Personas', #asignamos el titulo al eje y 
        xaxis_title_text=f'{factor_detalle_micro}', # asignamos el titulo al eje x
        bargap=0.0)  # Establece el espacio entre barras a 0 
    
    #se actualiza la configuracion del eje x 
    fig.update_xaxes(categoryorder='category ascending', dtick=10) #category order, nos ayuda a ordenar las etiquetas en orden ascendente y el dtick me ayuda a colocarle el nombre de los ejes cada cierto valor
    
    #Anotaciones para el total
    df_totals = df_seleccion.groupby(factor_detalle_micro).size().reset_index(name='Total')#creamos una copia del df para calcular la cantidad total de pacientes y se agrupa por la variable dinamica
    for index, row in df_totals.iterrows():# se crea un ciclo el cual itera sobre fila del df para poder procesar todos los totales de manera individual
        fig.add_annotation( #se agregan unas anotaciones especificas con posiciones definidas por mi
            x=row[factor_detalle_micro],y=row['Total'], #se define la posicion tanto en el eje x como en el y
            text=f"{int(row['Total'])}", #se convierte a int el valor agregado
            showarrow=False, #quita la flecha que señala la anotación
            yshift=10, #desplaza el texto cierta cantidad de pixeles
            xanchor='center',yanchor='bottom') #para x y para y va a centrar el texto de forma horizontal (x) y lo alinea en el eje y en la parte inferior

    st.plotly_chart(fig, use_container_width=True) #mostramos la figura en la pagina y el use es para que se ajuste automaticamente. 

with col_micro2: # para la columna 2 se a definir que es lo que lleva adentro
    st.markdown(f'### Promedio de {factor_detalle_micro} por Género y Rango de Edad') #aca me muestra el titulo de la seccion
    
    #a continuación definimos la lista de columnas que se necesitan para la grafica
    required_cols = ['Genero', 'Edad', factor_detalle_micro]
    df_clean = df_seleccion[required_cols].copy() # Creamos una copia para evitar SettingWithCopyWarning el cual es un error que ocurre cuando se intenta modificar un df que actua como una vista de otro
    df_clean[factor_detalle_micro] = pd.to_numeric(df_clean[factor_detalle_micro], errors='coerce') #convierte todos los valores de la variable directamente a formato de numero y el error cource es para evitar errores si hay valores que no puede convertir a numero
    df_clean = df_clean.dropna(subset=required_cols) #el dropna borra los valores nulos de todas las columnas especifcadas
    #A continuacion definimos los limites para agrupar las edades por el rango
    # el .arange nos ayuda a crear una matriz con valores que se espacian uniformemente
    # a partir del primer ( se crean los limites de edad en pasos de 5 años y al final se le suma 6 al valor maxim para asegurar que el ultimo valos de los datos se incluya en ese rango.
    bins = np.arange(df_clean['Edad'].min(), df_clean['Edad'].max() + 6, 5)
    # se usa f para darle formato a los strings y genera las etiquetas osea En cada iteración del bucle, el valor actual de i y el valor de i+4 se insertan en la cadena para formar una etiqueta de rango de edad.
    # for (por cada numero generado en la funcion range y asigna una variable i temporal ejemplo:El bucle itera a través de la secuencia, y en cada iteración, i toma el siguiente valor de la secuencia (20, luego 25, luego 30, y así sucesivamente).
    # con la funcion range el punto de partida es la edad minima  y final es el valor maximo +1 para que incluya el ultimo valor y el 5 son cada cuanto se incrementa el valor
    labels = [f'{i}-{i+4}' for i in range(df_clean['Edad'].min(), df_clean['Edad'].max() + 1, 5)]
    df_clean['Rango_Edad'] = pd.cut(df_clean['Edad'], bins=bins, labels=labels, right=False)

    # Agrupa el df_clean por 'Genero' y 'Rango_Edad', el .agg realiza como una operacion de agregacion que en este caso seria calcular el promedio  de la columna factor_detalle_micro
    # con el reset convierte el resultado en un df y resetea el index
    final_table = df_clean.groupby(['Genero', 'Rango_Edad']).agg(Promedio_Tabaquismo=(factor_detalle_micro, 'mean')).reset_index()
    
    # Redondear el promedio a 2 cifras decimales para una mejor presentación en el gráfico
    final_table['Promedio_Tabaquismo'] = final_table['Promedio_Tabaquismo'].round(2)
    
    # A continuacion se comienza la creacion del Gráfico de Líneas con Plotly Express
    fig_line = px.line(#se crea un grafico de lineas usando la libreria plotly
        final_table, #se define de donde se obtiene los datos
        x='Rango_Edad', #se establece la columna rango de edad en el eje x 
        y='Promedio_Tabaquismo',  # se establece la columna promedio tabaquismo en el eje y
        color='Genero', color_discrete_map=color_genero, # Separa las líneas por género y por color
        markers=True, # Añade marcadores a los puntos de datos
        labels={
            'Rango_Edad': 'Rango de Edad',
            'Promedio_Tabaquismo': f'Promedio de {factor_detalle_micro}'
        },
        template='plotly_white') # aplica como un estilo del fondo de la grafica

    # se hacen mas ajustes para el diseño del gráfico
    fig_line.update_layout(legend_title_text='Género', #cambia el titulo de las leyendas
        yaxis_range=[0, 100]) # Fija el rango del eje Y de 0 a 100%
    st.plotly_chart(fig_line, use_container_width=True)
print('Vamos bien')
