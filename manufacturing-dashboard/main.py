# Gyro A. Madrona - Electronics Engineer

# imports and packages
import streamlit as st
import pandas as pd
from datetime import timedelta, datetime

# set page config
st.set_page_config(page_title='Production Dashboard',layout='wide')

# helper functions
@st.cache_data
def load_data():
    data = pd.read_csv(r'dataset\manufacturing_dataset.csv')
    data['time_stamp'] = pd.to_datetime(data['time_stamp'])
    return data

def custom_quarter(date):
    month = date.month
    year = date.year
    if month in [2,3,4]:
        return pd.Period(year=year,quarter=1,freq='Q')
    elif month in [5,6,7]:
        return pd.Period(year=year,quarter=2,freq='Q')
    elif month in [8,9,10]:
        return pd.Period(year=year,quarter=3,freq='Q')
    else: # month in [11,12,1]
        return pd.Period(year=year if month !=1 else year-1, quarter=4, freq='Q')

def aggregate_data(df,freq):
    if freq == 'Q':
        df = df.copy()
        df['quarter'] = df['time_stamp'].apply(custom_quarter)
        df_agg = df.groupby('quarter').agg({
            'speed':'mean',
            'error_rate':'mean',
            'power_consumption':'sum'
        })
        return df_agg
    else:
        return df.resample(freq, on='time_stamp').agg({
            'speed':'mean',
            'error_rate':'mean',
            'power_consumption':'sum'
        })

def get_hourly_data(df):
    return aggregate_data(df,'H')

def get_daily_data(df):
    return aggregate_data(df,'D')
    
def get_weekly_data(df):
    return aggregate_data(df,'W-MON')

def get_monthly_data(df):
    return aggregate_data(df,'M')

def get_quarterly_data(df):
    return aggregate_data(df,'Q')

def format_with_commas(number):
    return f'{number:,}'

def create_metric_chart(df,column,color,height=150,time_frame='Daily'):
    chart_data = df[[column]].copy()
    if time_frame == 'Quarterly':
        chart_data.index = chart_data.index.strftime('%Y Q%q')
    st.line_chart(chart_data,y=column,color=color,height=height)

def is_period_complete(date, freq):
    today = datetime.now()
    if freq == 'D':
        return date.date() < today.date()
    elif freq == 'W':
        return date + timedelta(days=6) < today
    elif freq == 'M':
        next_month = date.replace(day=28) + timedelta(days=4)
        return next_month.replace(day=1) <= today
    elif freq == 'Q':
        current_quarter = custom_quarter(today)
        return date < current_quarter

# KPI: current-previous performance
def calculate_delta(df, column):
    if len(df) < 2:
        return 0,0
    current_value = df[column].iloc[-1]
    previous_value = df[column].iloc[-2]
    delta = current_value - previous_value
    delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
    return delta, delta_percent

def display_metric(col,title,value,df,column,color,time_frame):
    with col:
        with st.container(border=True):
            st.metric(label=title, 
                      value=format_with_commas(round(value, 2)),
                      help=f"Total {title.lower()} for selected period")
            delta,delta_percent = calculate_delta(df,column)
            delta_str = f'{delta:+,.0f} ({delta_percent:+.2f}%)'
            
            create_metric_chart(df,column,color,time_frame=time_frame)
            
            last_period = df.index[-1]
            freq = {'Hourly':'H','Daily': 'D', 'Weekly': 'W', 'Monthly': 'M', 'Quarterly': 'Q'}[time_frame]
            if not is_period_complete(last_period, freq):
                st.caption(f"Note: The last {time_frame.lower()[:-2] if time_frame != 'Daily' else 'day'} is incomplete.")
    
# load data
df = load_data()

# set up input widgets
st.logo(image=r'image\streamlit-logo-primary-colormark-lighttext.png', 
        icon_image=r'image\streamlit-mark-color.png')

with st.sidebar:
    st.title('Production Dashboard')
    
    max_date = df['time_stamp'].max().date()
    min_date = df['time_stamp'].min().date()
    
    default_start_date = max(min_date,max_date - timedelta(days=365))
    default_end_date = max_date
    start_date = st.date_input('Start date',default_start_date,
                               min_value=df['time_stamp'].min().date(),
                               max_value=max_date)
    end_date = st.date_input('End date',default_end_date,
                             min_value=df['time_stamp'].min().date(),
                             max_value=max_date)
    time_frame = st.selectbox('Select time frame',
                              ('Hourly','Daily','Weekly','Monthly','Quarterly'))
    
# Prepare data based on selected time frame
if time_frame == 'Hourly':
    df_display = get_hourly_data(df)
elif time_frame == 'Daily':
    df_display = get_daily_data(df)
elif time_frame == 'Weekly':
    df_display = get_weekly_data(df)
elif time_frame == 'Monthly':
    df_display = get_monthly_data(df)
elif time_frame == 'Quarterly':
    df_display = get_quarterly_data(df)

# Display Key Metrics
st.subheader('Statistics')
metrics = [
    ('Average Production Speed','speed','#126782'),
    ('Average Error Rate','error_rate','#126782'),
    ('Power Consumption','power_consumption','#126782')
]

cols = st.columns(3)
for col,(title,column,color) in zip(cols,metrics):
    value = df[column].mean()
    display_metric(col,title,value,df_display,column,color,time_frame)

