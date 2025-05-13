#imports and packages
import streamlit as st
import pandas as pd

# time frame
def get_hour(df):
    temp_data = df.copy()
    temp_data['date'] = temp_data['time_stamp'].dt.strftime('%Y-%m-%d-%H')
    return temp_data

def get_day(df):
    temp_data = df.copy()
    temp_data['date'] = temp_data['time_stamp'].dt.date
    return temp_data

def get_month(df):
    temp_data = df.copy()
    temp_data['date'] = temp_data['time_stamp'].dt.strftime('%b')
    
    months_order = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']
    temp_data['date'] = pd.Categorical(temp_data['date'],
                                       categories=months_order,
                                       ordered=True)
    
    return temp_data

def get_year(df):
    temp_data = df.copy()
    temp_data['date'] = temp_data['time_stamp'].dt.strftime('%Y')
    return temp_data