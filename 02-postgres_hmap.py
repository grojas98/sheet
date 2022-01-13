# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:20:37 2022

@author: groja
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import psycopg2 as pg

#%% DATABASE CONNECTION

#connect to db
con = pg.connect(
    host = '192.168.1.101',
    user = 'postgres',
    password = 'somno2019',
    port = '9001',
    database = 'somno')

#cursor
cur = con.cursor()

postgreSQL_select_Query = "select * from mac_94b97ec06258 order by time desc limit 1"




#%%
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Mapa de calor Sabanilla')

st.markdown("""
Figura con mapa de calor actualizado en tiempo real
con números **aleatorios**.
""")

hm_df = pd.DataFrame()

state = 0

fig, ax = plt.subplots()

heat_map = st.empty()
# series_graph = st.empty()

start = st.button('Start simulation')

if start:
    state = 1

stop = st.button('Stop')

if state == 1:
    while True:
        plt.close(fig)
        fig, ax = plt.subplots()
        cur.execute(postgreSQL_select_Query)
        mobile_records = cur.fetchall()
        sens = list(mobile_records[0][1:])
        df_data = {
            'col1': [sens[17],sens[20],sens[23]],
            'col2': [sens[8],sens[11],sens[14]],
            'col3': [sens[7],sens[10],sens[0]],
            'col4': [sens[21],sens[1],sens[4]],
            'col5': [sens[12],sens[15],sens[18]],
            'col6': [sens[3],sens[6],sens[9]],
            'col7': [sens[19],sens[2],sens[5]],
            'col8': [sens[13],sens[16],sens[19]]
        }
        
        hm_df = pd.DataFrame.from_dict(df_data)
        sns.heatmap(hm_df,vmin=0,vmax=4068,annot=True,fmt='.0f',ax=ax,square=True)
        heat_map.write(fig)
        time.sleep(0.5)
        if stop:
            state = 0
            break

    

#close cursor
cur.close()

#close connection
con.close()
