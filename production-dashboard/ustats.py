# imports and packages
import streamlit as st

# statistics
def get_kpi_df(df):
    ''''
    - Adds 'yield' which is 100% - defect_rate
    - Adds 'up_time' by simply labeling each row as 1-minute
    - Aggregrate key metrics and returns the df
    '''
    df = df.copy()
    df = df[['time_stamp','operation_mode','defect_rate','speed']]
    df['yield'] = df['defect_rate'].apply(lambda data: 100-data )
    df['time_duration'] = df['operation_mode'].apply(lambda data: 1) # in minute
    df = df.groupby(['time_stamp','operation_mode']).agg({
        'defect_rate':'mean',
        'yield':'mean',
        'speed':'mean',
        'time_duration':'sum'
    }).reset_index()
    return df
    
