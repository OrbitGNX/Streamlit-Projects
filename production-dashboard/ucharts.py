# imports and packages
import streamlit as st
import plotly.express as px

'''
- Displays a selected chart:
- x-axis = 'time_stamp'
- y-axis = depends on the kpi
'''

def display_line_chart(df,kpi):
    if kpi == 'Yield Trend':
        y=df['yield']
        y_label='%'
    elif kpi == 'Output Trend':
        y=df['output']
        y_label='units'
        
    fig = px.line(df,
                  x='time_stamp',
                  y=y,
                  title=kpi,
                  height=300)
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_label
    )
    st.plotly_chart(fig,use_container_width=True)
    
def display_bar_chart(df,kpi):
    if kpi == 'Operation Mode':
        x = df['operation_mode']
        y = df['percentage']
        y_label = '%'
    
    fig = px.bar(df,
                  x=x,
                  y=y,
                  title=kpi,
                  text_auto='.1f',
                  height=300)
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title=y_label,
    )
    fig.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='inside'
    )
    st.plotly_chart(fig,use_container_width=True)
    
def display_area_chart(df,kpi):
    if kpi == 'Yield Trend':
        y=df['yield']
        y_label='%'
    elif kpi == 'Output Trend':
        y=df['output']
        y_label='units'
        
    fig = px.area(df,
                  x='time_stamp',
                  y=y,
                  title=kpi,
                  height=300)
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_label,
        yaxis_range=[min(y),max(y)]
    )
    st.plotly_chart(fig,use_container_width=True)
    
def display_donut_chart(df,kpi):
    if kpi == 'Operation Mode':
        names=df['operation_mode']
        values=df['percentage']
        y_label='%'
        
    fig = px.pie(df,
                  names=names,
                  values=values,
                  hole=0.5,
                  title=kpi,
                  height=300)
    st.plotly_chart(fig,use_container_width=True)