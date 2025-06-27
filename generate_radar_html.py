# generate_radar_html.py

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1) Cargo y mergeo los datos de 2023
# — GDP
df_gdp = (
    pd.read_csv('Proyecto-IPC/gdp-per-capita-worldbank.csv', thousands=',', decimal='.')
      .query('Year==2023 and Entity!="World"')
      .rename(columns={'GDP per capita, PPP (constant 2021 international $)':'GDP_per_capita'})
      [['Entity','GDP_per_capita']]
)

# — Felicidad
df_hap = (
    pd.read_csv('Proyecto-IPC/happiness-cantril-ladder.csv')
      .query('Year==2023 and Entity!="World"')
      .rename(columns={'Cantril ladder score':'Happiness_score'})
      [['Entity','Happiness_score']]
)

# — Factores extra
df_extra = (
    pd.read_csv('Proyecto-IPC/World Happiness Report (1).csv', thousands=',', decimal='.')
      .drop(columns=['Happiness Score','Economy','Happiness Rank'])
      .rename(columns={'Country':'Entity'})
      [['Entity','Family','Health','Freedom','Generosity','Corruption','Job Satisfaction']]
)

df = df_gdp.merge(df_hap,on='Entity').merge(df_extra,on='Entity')

# 2) Defino las categorías (sin “Dystopia”)
categories = ['GDP_per_capita','Happiness_score','Family',
              'Health','Freedom','Generosity','Corruption','Job Satisfaction']

# 3) Normalizo cada columna a [0,1]
for c in categories:
    mn, mx = df[c].min(), df[c].max()
    df[c] = (df[c] - mn) / (mx - mn)

# 4) Construyo la figura con un trace por país (sólo uno visible al inicio)
fig = go.Figure()
for i, country in enumerate(df['Entity']):
    vals = df.loc[i, categories].tolist()
    vals += [vals[0]]   # cerrar polígono
    thetas = categories + [categories[0]]

    fig.add_trace(go.Scatterpolar(
        r=vals,
        theta=thetas,
        fill='toself',
        name=country,
        visible=(i==0)
    ))

# 5) Botones de dropdown: cada botón muestra sólo el trace correspondiente
buttons = []
for i, country in enumerate(df['Entity']):
    vis = [False]*len(df)
    vis[i] = True
    buttons.append(dict(label=country,
                        method='update',
                        args=[{'visible': vis},
                              {'title': f'Radar: {country}'}]))

fig.update_layout(
    updatemenus=[dict(active=0,
                      buttons=buttons,
                      x=0.1, y=1.15,
                      xanchor='left', yanchor='top')]
)

fig.update_layout(
    title=f'Radar: {df["Entity"].iloc[0]}',
    polar=dict(
        radialaxis=dict(visible=True, range=[0,1])
    ),
    margin=dict(l=50,r=50,t=100,b=50)
)

# 6) Exporto HTML auto-contenible
fig.write_html('index.html', include_plotlyjs='cdn', full_html=True)
print("👉 index.html generado ✅")
