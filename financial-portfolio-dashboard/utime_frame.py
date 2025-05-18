#imports and packages
import streamlit as st
import pandas as pd

# time frame
def get_day(df):
    df = df.copy()
    df['Date'] = df['Date'].dt.date
    return df

def get_month(df):
    df = df.copy()
    df['Date'] = df['Date'].dt.strftime('%Y-%b') # 2024-Jan
    min_date = pd.to_datetime(df['Date'],format='%Y-%b').min()
    max_date = pd.to_datetime(df['Date'],format='%Y-%b').max()
    
    months_order = pd.date_range(
        start=min_date,
        end=max_date,
        freq='MS' # Month Start
    ).strftime('%Y-%b').tolist()

    df['Date'] = pd.Categorical(df['Date'],
                                       categories=months_order,
                                       ordered=True)
    return df

def get_year(df):
    df = df.copy()
    df['Date'] = df['Date'].dt.strftime('%Y')
    return df