'''
 My Financial Portfolio Dashboard
 Developer: Gyro A. Madrona
'''
# imports and packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime,timedelta

import utime_frame as utf
import ustats as ustats
import ucharts

# set page config
st.set_page_config(page_title='Financial Portfolio',layout='wide')

with st.sidebar:
    st.logo(image='financial-portfolio-dashboard/image/gyronix-with-text.png',
        icon_image='financial-portfolio-dashboard/image/gyronix-logo.png')
    
    st.title('📊Financial Portfolio')
    
    # upload cash-flow dataset
    raw = st.file_uploader('upload a CSV file',type='csv')

# dataset
@st.cache_data
def load_data(raw):
    # raw = pd.read_csv(r"raw\my-cash-flow.csv")
    if raw is None:
        st.warning('Please upload a csv file to continue.')
        st.stop()
    
    raw = pd.read_csv(raw)
    raw['Date'] = pd.to_datetime(raw['Date'])
    return raw

# sidebar
with st.sidebar:
    # load dataset
    df = load_data(raw)
    
    #  Set date range
    max_date = df['Date'].max()
    min_date = df['Date'].min()
    default_start_date = max_date - timedelta(days=90)
    default_end_date = max_date
    
    start_date = st.date_input('Start date',default_start_date)
    end_date = st.date_input('End date',default_end_date)
    
    # filter data
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)
    df = df[(df['Date'] >= start_datetime) & 
                 (df['Date'] < end_datetime)]
    
    time_frame = st.selectbox('Select time frame',
                              ('day','month','year'),index=1)
    
    # prepare data based on selected time frame
    if time_frame == 'day':
        filtered_df = utf.get_day(df)
    elif time_frame == 'month':
        filtered_df = utf.get_month(df)
    elif time_frame == 'year':
        filtered_df = utf.get_year(df)

# Filtered df
expenses_df, expenses_df_with_date = ustats.get_expenses_df(filtered_df)
cum_df = ustats.get_cum_df(filtered_df)

st.write(start_date,"-", end_date)
kpi = st.columns(3)
with kpi[0]: # Cash-In
    with st.container(border=True):
        total_cash_in = cum_df['cum_in'].iloc[-1]
        current_in = cum_df['In'].iloc[-1]
        previous_in = cum_df['In'].iloc[-2] if len(cum_df) > 1 else 0
        delta_in = current_in - previous_in
        
        st.metric('Total Cash-In',
                  value=f'{total_cash_in:,.0f}',
                  delta=f'{delta_in:,.0f} this {time_frame}')
           
with kpi[1]: # Cash-Out
    with st.container(border=True):
        total_cash_out = cum_df['cum_out'].iloc[-1]
        current_out = cum_df['Out'].iloc[-1]
        previous_out = cum_df['Out'].iloc[-2] if len(cum_df) > 1 else 0
        delta_out = current_out - previous_out
        
        st.metric('Total Expenses',
                  value=f'{total_cash_out:,.0f}',
                  delta=f'{delta_out:,.0f} this {time_frame}',
                  delta_color='inverse')

with kpi[2]: # Savings
    with st.container(border=True):
        total_savings = cum_df['cum_savings'].iloc[-1]
        
        current_saving = cum_df['savings'].iloc[-1]
        previous_saving = cum_df['savings'].iloc[-2] if len(cum_df) > 1 else 0
        # 'savings' can be negative since it is = 'In' - 'Out'
        delta_saving = current_saving + previous_saving
                
        st.metric('Total Savings',
                  value=f'{total_savings:,.0f}',
                  delta=f'{delta_saving:,.0f} this {time_frame}')

chart = st.columns(2)
with chart[0]:# Cash Flow Trend
    with st.container(border=True):
        ucharts.display_line_chart(cum_df,'Cumulative Cash Flow Trend',time_frame)
        with st.expander('see dataframe'):
            st.dataframe(cum_df[['Date','In','Out','savings']])

with chart[1]: # Expenses Pareto Chart
    with st.container(border=True):
        ucharts.display_pareto_chart(expenses_df,'Expenses Pareto Chart')
        with st.expander('see dataframe'):
            st.dataframe(expenses_df_with_date)
