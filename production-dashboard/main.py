# imports and packages
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta,datetime

import ustats
import ucharts
import utime_frame as utf

# Set page config
st.set_page_config(page_title="Production Dashboard",layout="wide")

# Layout
period = st.columns(1)
tab = st.tabs(['KPI','Other Metrics'])

# dataset
@st.cache_data
def load_data():
    raw = pd.read_csv(r"production-dashboard\dataset\manufacturing_dataset.csv")
    raw['time_stamp'] = pd.to_datetime(raw['time_stamp'])
    return raw

# Load data
df = load_data()

# side bar
st.logo(image="production-dashboard/image/streamlit-logo-primary-colormark-lighttext.png", 
        icon_image="production-dashboard/image/streamlit-mark-color.png")

with st.sidebar:
    st.title('Production Dashboard')
    
    # production date
    max_date = df['time_stamp'].max()
    min_date = df['time_stamp'].min()
    default_start_date = max_date - timedelta(days=30)
    default_end_date = max_date
    
    start_date = st.date_input('Start date',default_start_date)
    end_date = st.date_input('End date',default_end_date)
    
    # filter data
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)
    df = df[(df['time_stamp'] >= start_datetime) & 
                 (df['time_stamp'] < end_datetime)]
    
    time_frame = st.selectbox('Select time frame',
                              ('hour','day','month','year'),index=1)
    
    # prepare data based on selected time frame
    if time_frame == 'hour':
        metric_data = utf.get_hour(df)
    elif time_frame == 'day':
        metric_data = utf.get_day(df)
    elif time_frame == 'month':
        metric_data = utf.get_month(df)
    elif time_frame == 'year':
        metric_data = utf.get_year(df)
 
# Metrics
kpi_df = ustats.get_kpi_df(metric_data)
active_mode_df = (kpi_df[kpi_df['operation_mode']=='Active']).dropna()

with tab[0]: # KPI
    # layout
    kpi = st.columns(3)
    chart = st.columns(3)
    
    with period[0]:
        st.write(start_date,"-",end_date)

    with kpi[0]: # Production Yield
        with st.container(border=True):
            current_yield = active_mode_df['yield'].iloc[-1]
            previous_yield = active_mode_df['yield'].iloc[-2] if len(active_mode_df) > 1 else 0
            yield_delta = current_yield - previous_yield
            
            st.metric('Production Yield',
                    value=f'{current_yield:.2f}',
                    delta=f'{yield_delta:.2f} % this {time_frame}')

    with kpi[1]: # Production Output
        with st.container(border=True):
            speed_df = active_mode_df.copy()
            # based speed is units/min
            if time_frame == 'hour':
                time_frame_mul = 60
            elif time_frame == 'day':
                time_frame_mul = timedelta(days=1).total_seconds()/60
            elif time_frame == 'month':
                time_frame_mul = timedelta(days=30).total_seconds()/60
            elif time_frame == 'year':
                time_frame_mul = timedelta(days=365).total_seconds()/60
            
            speed_df['output'] = speed_df['speed'].apply(lambda data: data*time_frame_mul)
            current_speed = speed_df['output'].iloc[-1]
            previous_speed = speed_df['output'].iloc[-2] if len(active_mode_df) > 1 else 0
            speed_delta = current_speed - previous_speed
            
            st.metric('Production Output',
                    value=f'{current_speed:,.0f}',
                    delta=f'{speed_delta:,.0f} units this {time_frame}')
            
    with kpi[2]: # Uptime
        with st.container(border=True):
            current_uptime = (active_mode_df['time_duration'].iloc[-1])/60
            previous_uptime = (active_mode_df['time_duration'].iloc[-2])/60 if len(active_mode_df) > 1 else 0
            uptime_delta = current_uptime - previous_uptime
            
            st.metric('Production Uptime',
                    value=f'{current_uptime:.2f}',
                    delta=f'{uptime_delta:.2f} hours this {time_frame}')

    with chart[0]: # Yield Trend
        with st.container(border=True):
            ucharts.display_line_chart(active_mode_df,'Yield Trend')
            with st.expander('see dataframe'):
                st.dataframe(active_mode_df[['time_stamp','yield','defect_rate']])
        
    with chart[1]: # Output Trend
        with st.container(border=True):
            ucharts.display_line_chart(speed_df,'Output Trend')
            with st.expander('see dataframe'):
                st.dataframe(speed_df[['time_stamp','output']])
    
    with chart[2]: # Operation Mode Trend
        with st.container(border=True):
            opmode_df = kpi_df.groupby(['time_stamp','operation_mode'])['time_duration'].sum().reset_index()
            current_opmode = opmode_df[opmode_df['time_duration']!=0].tail(3)
            # pecentage = (active_time/total_time)...idle_time/ ...maintenance_time/...
            current_opmode['percentage'] = current_opmode['time_duration'].apply(
                (lambda data:(data/current_opmode['time_duration'].sum()*100)))
            ucharts.display_bar_chart(current_opmode,'Operation Mode')
            with st.expander('see dataframe'):
                st.dataframe(opmode_df[opmode_df['time_duration']!=0])

with tab[1]: # Other Metrics
    # layout
    kpi = st.columns(3)
    chart = st.columns(3)
    
    with kpi[0]:
        with st.container(border=True):
            st.metric('another KPI',
                    value=0,
                    delta=0)
    with kpi[1]:
        with st.container(border=True):
            st.metric('another KPI',
                    value=0,
                    delta=0)
    with kpi[2]:
        with st.container(border=True):
            st.metric('another KPI',
                    value=0,
                    delta=0)
    
    with chart[0]: # Yield Trend
        with st.container(border=True):
            ucharts.display_area_chart(active_mode_df,'Yield Trend')
            with st.expander('see dataframe'):
                st.dataframe(active_mode_df[['time_stamp','yield','defect_rate']])
    
    with chart[1]: # Output Trend
        with st.container(border=True):
            ucharts.display_area_chart(speed_df,'Output Trend')
            with st.expander('see dataframe'):
                st.dataframe(speed_df[['time_stamp','output']])
    
    with chart[2]: # Operation Mode Trend
        with st.container(border=True):
            opmode_df = kpi_df.groupby(['time_stamp','operation_mode'])['time_duration'].sum().reset_index()
            current_opmode = opmode_df[opmode_df['time_duration']!=0].tail(3)
            # pecentage = (active_time/total_time)...idle_time/ ...maintenance_time/...
            current_opmode['percentage'] = current_opmode['time_duration'].apply(
                (lambda data:(data/current_opmode['time_duration'].sum()*100)))
            ucharts.display_donut_chart(current_opmode,'Operation Mode')
            with st.expander('see dataframe'):
                st.dataframe(opmode_df[opmode_df['time_duration']!=0])
