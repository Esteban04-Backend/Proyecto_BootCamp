import pandas as pd
df=pd.read_csv('data/cancer-risk-factors.csv')
print('\nBase de Datos sin Tratar')
print(df.head())
df.drop(['Patient_ID'], axis=1, inplace=True)
df.rename(columns={'Cancer_Type':'Tipo_de_Cancer', 'Age':'Edad','Gender':'Genero'}, inplace=True)
df['Tipo_de_Cancer']=df['Tipo_de_Cancer'].replace('Prostate','Prostata').replace('Skin','Piel').replace('Lung','Pulmon').replace('Breast','Seno') 
df['Genero']=df['Genero'].replace(0,'Femenino').replace(1,'Masculino') #Se cambio el 0 por femenino y el 1 por Masculino
print('\nBase de datos Tratada')
print(df.head())
#Contar segun edad y Genero
grupos=df.groupby(['Genero'])['Edad'].count()
print(grupos)