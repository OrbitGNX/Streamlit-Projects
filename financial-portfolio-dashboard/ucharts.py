# imports and packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
- Displays a selected chart:
- x-axis = 'time_stamp'
- y-axis = depends on the kpi
'''

def display_line_chart(df,kpi,time_frame):
    if kpi == 'Cumulative Cash Flow Trend':
        df = df.melt(
            id_vars='Date',
            var_name='Flow',
            value_vars=['cum_in','cum_out','cum_savings'],
            value_name='Amount'
        )
        y='Amount'
        y_label='PHP' 
    
    fig = px.line(df,
                  x='Date',
                  y=y,
                  title=kpi,
                  color='Flow',
                  markers=True,
                  height=300)
    
    if time_frame == 'year': # to prevent 2023.5 year
        fig.update_xaxes(
            dtick=1,
            tickformat='d'
        )
        
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_label
    )
    st.plotly_chart(fig,use_container_width=True)
    
def display_pareto_chart(df,kpi):
    if kpi == 'Expenses Pareto Chart':
        x = 'Category'
        y1 = 'Amount'
        y1_label = 'PHP'
        
        y2 = 'cum_percentage'
        y2_label = '%'
    
    fig = px.bar(df,
                 x=x,
                 y=y1,
                 title=kpi,
                 text_auto=',.0f',
                 height=300).update_traces(textposition='inside')
    
    # line chart on secondary y-axis
    fig.add_trace(go.Scatter(
        x=df[x],
        y=df[y2],
        name='Cumulative %',
        yaxis='y2',
        showlegend=False
        ))
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title=y1_label,
        
        yaxis2=dict(
            title=y2_label,
            overlaying='y',
            side='right',
            range=[0,100],
            tickformat='0.f%',
            showgrid=False
        ),
        hovermode='x unified'
    )
    st.plotly_chart(fig,use_container_width=True)