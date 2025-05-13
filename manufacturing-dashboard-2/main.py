# imports and packages
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta,datetime

import ustats
import ucharts
import utime_frame as utf

# Set page config
st.set_page_config(page_title="Produtction Dashboard",layout="wide")

# Layout
metric_1, metric_2, metric_3 = st.columns(3)

# dataset
@st.cache_data
def load_data():
    raw = pd.read_csv(r"dataset\manufacturing_dataset.csv")
    raw['time_stamp'] = pd.to_datetime(raw['time_stamp'])
    return raw

# Load data
df = load_data()

# side bar
st.logo(image="image/streamlit-logo-primary-colormark-lighttext.png", 
        icon_image="image/streamlit-mark-color.png")

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
    end_datetime = pd.to_datetime(end_date)
    df = df[(df['time_stamp'] >= start_datetime) & 
                 (df['time_stamp'] < end_datetime)]
    
    time_frame = st.selectbox('Select time frame',
                              ('Hour','Day','Month','Year'),index=1)

# prepare data based on selected time frame
if time_frame == 'Hour':
    metric_data = utf.get_hour(df)
elif time_frame == 'Day':
    metric_data = utf.get_day(df)
elif time_frame == 'Month':
    metric_data = utf.get_month(df)
elif time_frame == 'Year':
    metric_data = utf.get_year(df)
    
# Metrics
metric_agg = ustats.metric_agg(metric_data)
metric_count = ustats.metric_count(metric_data)
st.write(metric_count)

with metric_1:
    st.markdown("<h1 style='font-size:18px'>Production Speed</h1>", unsafe_allow_html=True)
    speed_mean = metric_agg['speed'].mean().round(1)
    st.markdown(f"<h1>{speed_mean} <span style='font-size:16px'>units/{time_frame}</span></h1>", unsafe_allow_html=True)
    ucharts.display_line_chart(metric_agg[['date','speed']],time_frame,'units')
    
with metric_2:
    st.markdown("<h1 style='font-size:18px'>Defect Rate</h1>", unsafe_allow_html=True)
    defect_mean = metric_agg['defect_rate'].mean().round(1)
    st.markdown(f"<h1>{defect_mean} <span style='font-size:16px'>%/{time_frame}</span></h1>", unsafe_allow_html=True)
    ucharts.display_line_chart(metric_agg[['date','defect_rate']],time_frame,'%') 
    
with metric_3:
    st.markdown("<h1 style='font-size:18px'>Operation Mode</h1>", unsafe_allow_html=True)
    active_mode = metric_count[metric_count['operation_mode']=='Active']['count']
    total_count = metric_count['count'].sum()
    active_percentage = (((active_mode/total_count)*100).round(1))[0]
    st.markdown(f"<h1>{active_percentage} <span style='font-size:16px'>% active/{time_frame}</span></h1>", unsafe_allow_html=True)
    ucharts.display_bar_chart(metric_count,time_frame,'%') 