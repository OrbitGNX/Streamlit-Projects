#imports and packages
import streamlit as st
import pandas as pd

# time frame
def get_hour(df):
    df = df.copy()
    df['time_stamp'] = df['time_stamp'].dt.strftime('%m/%d/%Y %H')
    return df

def get_day(df):
    df = df.copy()
    df['time_stamp'] = df['time_stamp'].dt.date
    return df

def get_month(df):
    df = df.copy()
    df['time_stamp'] = df['time_stamp'].dt.strftime('%b')
    
    months_order = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']
    df['time_stamp'] = pd.Categorical(df['time_stamp'],
                                       categories=months_order,
                                       ordered=True)
    return df

def get_year(df):
    df = df.copy()
    df['time_stamp'] = df['time_stamp'].dt.strftime('%Y')
    return df