import pandas as pd
df=pd.read_csv('data/cancer-risk-factors.csv')
print('\nBase de Datos sin Tratar')
print(df.head())
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
#df.to_excel('Cancer.xlsx', index=False)
print('Se creo el archivo Excel Correctamente')