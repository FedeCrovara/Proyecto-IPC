# 2) Importar librerías
import numpy as np
import pandas as pd

# 3) Leer las bases de datos
#    - Si están en CSV:
df1 = pd.read_csv('happiness-cantril-ladder.csv')
df2 = pd.read_csv('gdp-per-capita-worldbank.csv')
#    - O bien, si prefieres Excel:
# df1 = pd.read_excel('base1.xlsx', sheet_name='Hoja1')
# df2 = pd.read_excel('base2.xlsx', sheet_name='Hoja1')

# 4) Exploración rápida
print(df1.shape, df2.shape)
display(df1.head(), df2.head())

# 5) Limpieza y transformación básica
def clean_df(df):
    # 5.1) Normalizar nombres de columnas
    df.columns = (df.columns
                    .str.strip()                   # quitar espacios
                    .str.lower()                   # a minúsculas
                    .str.replace(' ', '_'))        # guiones bajos

    # 5.2) Eliminar duplicados
    df = df.drop_duplicates()

    # 5.3) Convertir fechas (si tienes columnas tipo fecha)
    fecha_cols = [c for c in df.columns if 'fecha' in c]
    for c in fecha_cols:
        df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')

    # 5.4) Revisar nulos y decidir política
    #    Por ejemplo, rellenar con ceros en columnas numéricas:
    num_cols = df.select_dtypes(['number']).columns
    df[num_cols] = df[num_cols].fillna(0)

    #    O bien, si prefieres eliminar filas con NA:
    # df = df.dropna(subset=['columna_clave'])

    return df

df1 = clean_df(df1)
df2 = clean_df(df2)

# 6) Guardar versión limpia (opcional)
df1.to_csv('../clean/base1_clean.csv', index=False)
df2.to_csv('../clean/base2_clean.csv', index=False)

# 7) Ya puedes empezar el análisis exploratorio:
corr1 = df1.corr()
corr2 = df2.corr()
print(corr1, corr2)
