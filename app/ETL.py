import pandas as pd
import os

def load_data_from_file(datapath, filename):
    path = os.path.join(datapath,filename)
    return pd.read_csv(path).assign(jaar =  filename.split('_')[2][:4],
                                                         dso = filename.split('_')[0])

def load_data(basepath='C:/Data/Code/EnergieKaart/data', type = 'Electricity'):
    datapath = os.path.join(basepath,type)
    files = os.listdir(datapath)
    files = [filename for filename in files if int(filename.split('_')[2][:4])>= 2017]
    # first file
    file = files[0]
    df = load_data_from_file(datapath,file)

    # loop over other files
    for file in files[1:]:
        temp_df = load_data_from_file(datapath,file)
        df = pd.concat([df,temp_df])
    return df

def calculate_top_ten(df, year, dso):
    df['Verbruik'] = [int(vb /1000) for vb in df['annual_consume']]
    df = df[df['dso']==dso].filter(['Verbruik','jaar','city'])
    df = (
        df.groupby(['jaar','city'])
            .agg('sum')
            .sort_values('Verbruik',ascending=False)
            .reset_index()
    )
    df = df[df['jaar'] == str(year)].iloc[:10,1:]
    df.columns = ['Stad', 'Jaarverbruik (MWh)']
    return df

def calculate_timeseries(df_elec, df_gas, cities):
    df_elec = (
        df_elec.assign(E = df_elec['annual_consume'])
            .set_index(['city','zipcode_from','zipcode_to','jaar'])
            .filter(['E','num_connections'])
        .drop_duplicates()
    )
    df_gas = (
        df_gas.assign(G = df_gas['annual_consume'])
            .set_index(['city','zipcode_from', 'zipcode_to', 'jaar'])
            .filter(['G','dso'])
        .drop_duplicates()
    )
    df = df_gas.join(df_elec).reset_index()
    df = (
        df.assign(Jaar = df['jaar'],
        Stad = df['city'],
        Verbruik = [(df['E'][i]*3.6 + df['G'][i]*35.17) for i in range(df.shape[0])])
            .filter(['Stad','Jaar','Verbruik','num_connections'])
            .groupby(['Stad','Jaar'])
            .agg('sum')
            .reset_index()
    )
    df['Gemiddeld_verbruik'] = [df['Verbruik'][i]/df['num_connections'][i] for i in range(df.shape[0])]
    df = df[[any([stad == Stad for stad in cities]) for Stad in df['Stad']]]
    return df