# imports and packages
import streamlit as st

# statistics
def metric_agg(df):
    temp_data = df.copy()
    # average by hour or day or month...
    temp_data = temp_data.groupby('date').agg({
        'speed':'mean',
        'defect_rate':'mean'
    }).reset_index()
    return temp_data

def metric_count(df):
    temp_data = df.copy()
    temp_data = temp_data.groupby('machine_ID')['operation_mode'].value_counts().reset_index()
    return temp_data
