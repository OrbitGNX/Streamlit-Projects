import streamlit as st 
import pandas as pd 

def get_expenses_df(df):
    df = df.copy()
    df = df[df['Flow']=='Out']
    df_with_date = df.groupby(['Date','Category'])['Amount'].sum().reset_index()
    df = df.groupby('Category')['Amount'].sum().reset_index()
    df = df[df['Amount']!=0]
    total_expenses = df['Amount'].sum()
    df['percentage'] = df['Amount'].apply(lambda data: (data/total_expenses)*100)
    df = df.sort_values(by='Amount',ascending=False)
    df['cum_percentage'] = df['percentage'].cumsum()
    return df,df_with_date

def get_cum_df(df):
    df = df.copy()
    
    df = df.groupby(['Date','Flow'])['Amount'].sum().reset_index()
    df = df[df['Amount']!=0]
    
    # split 'In' and 'Out' into two columns
    df = df.pivot(index='Date',
                  columns='Flow',
                  values='Amount').fillna(0).reset_index()
    df['cum_in'] = df['In'].cumsum()
    df['cum_out'] = df['Out'].cumsum()
    df['savings'] = df['In'] - df['Out']
    df['cum_savings'] = df['savings'].cumsum()
    return df
    