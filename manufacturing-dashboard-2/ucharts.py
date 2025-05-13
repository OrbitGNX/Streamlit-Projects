# imports and packages
import streamlit as st
import plotly.express as px

def display_line_chart(df,time_frame,unit):
    fig = px.line(df,
                  x='date',
                  y=df.columns[1],
                  title=f'{time_frame} Trend')
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title=unit
    )
    st.plotly_chart(fig,use_container_width=True)
    
def display_bar_chart(df,time_frame,unit):
    fig = px.bar(df,
                  x=df.columns[0],
                  y=df.columns[1],
                  title='N Counts')
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='counts'
    )
    st.plotly_chart(fig,use_container_width=True)