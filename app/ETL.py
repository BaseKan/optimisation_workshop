import pandas as pd
import os
import numpy as np

def load_data_from_file(datapath, filename):
    path = os.path.join(datapath,filename)
    return pd.read_csv(path).assign(jaar =  filename.split('_')[2][:4],
                                                         dso = filename.split('_')[0])

def load_timeseries_data(basepath='/Users/tim/Documents/Tutorials/Kennissessie-optimalisatie/optimisation_workshop/data', type = 'Electricity'):
    datapath = os.path.join(basepath,type)
    files = os.listdir(datapath)
    files = [filename for filename in files if int(filename.split('_')[2][:4])>= 2017]
    dsos = ['liander','enexis','stedin']
    files = [filename for filename in files if any(dso in filename for dso in dsos)]
    df = pd.concat([load_data_from_file(datapath, file) for file in files])
    return df

def calculate_top_ten(df):
    df = df.assign(Verbruik = df['annual_consume']).filter(['Verbruik','city'])
    df = (
        df.filter(['city','Verbruik']).
            groupby(['city'])
            .agg(np.sum)
            .sort_values('Verbruik',ascending=False)
            .reset_index()
            .iloc[:10,:]
    )
    df.columns = ['Stad', 'Jaarverbruik (MWh)']
    return df

def calculate_timeseries(df_elec, df_gas, cities):
    df_elec = (
        df_elec.query(f'city in {cities}')
            .filter(['city','jaar','annual_consume','num_connections'])
            .groupby(['city','jaar'])
            .agg(np.sum)
    )
    df_elec.columns = ['E','num_connections']
    df_gas = (
        df_gas.query(f'city in {cities}')
            .filter(['city','jaar', 'annual_consume'])
            .groupby(['city', 'jaar'])
            .agg(np.sum)
    )
    df_gas.columns = ['G']
    df = df_gas.join(df_elec).reset_index()
    df = (
        df.assign(Gemiddeld_verbruik = (df['E']*3.6 + df['G']*35.17)/df['num_connections'])
        .filter(['city','jaar','Gemiddeld_verbruik'])
    )
    df.columns = ['Stad','Jaar','Gemiddeld_verbruik']
    return df