'''
LOGS DATA OF TUMLIVE
'''

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Common layout settings
layout_settings = {
    'title_font_size': 64,
    'xaxis_title_font_size': 48,
    'yaxis_title_font_size': 48,
    'xaxis_tickfont_size': 32,
    'yaxis_tickfont_size': 32,
    'legend_font_size': 32,
    'font_family': 'LaTeX'
}

file_path = './data/TUM-Live Service errors-data-2024-08-11 23_35_47.csv'
new_df = pd.read_csv(file_path)

new_df['Time'] = pd.to_datetime(new_df['Time'], errors='coerce')
new_df = new_df.dropna(subset=['Time'])
new_df.set_index('Time', inplace=True)

# Extract log levels and messages (handle both errors and warnings)
extracted_logs = new_df['Line'].str.extract(r'"level":"(ERROR|WARN)","msg":"([^"]+)"')
new_df['level'] = extracted_logs[0]
new_df['message'] = extracted_logs[1]

# Filter error logs
error_logs = new_df[new_df['level'] == 'ERROR']

# Analyze error logs over time by counting occurrences per day
error_logs_over_time = error_logs.resample('D').size()

# Step 1: Rolling Window to Smooth Data
error_logs_smoothed = error_logs_over_time.rolling(window=6, min_periods=1).mean()

# Step 2: Synthetic Data Generation for Scaling Up
# Generate synthetic data by slightly shifting existing error logs in time
synthetic_logs = error_logs.copy()
synthetic_logs.index += pd.to_timedelta(np.random.randint(1, 60, size=len(synthetic_logs)), unit='m')

# Append synthetic logs to the original dataset
combined_error_logs = pd.concat([error_logs, synthetic_logs])
combined_error_logs_over_time = combined_error_logs.resample('h').size()

# Count occurrences of each error type
error_types = error_logs['message']
error_type_counts = error_types.value_counts()

# Daily Error Rate Analysis: Normalize errors over total logs to show the rate
total_logs_per_day = new_df.resample('D').size()
error_rate = (error_logs_over_time / total_logs_per_day).fillna(0) * 100  # Convert to percentage

# Trend analysis using rolling average
error_trend = error_logs_over_time.rolling(window=6).mean()  # 6-day rolling average

# Group error logs by Hour and Error Type (Message)
error_logs.loc[:, 'Hour'] = error_logs.index.hour
error_logs_grouped = error_logs.groupby(['Hour', 'message']).size().unstack(fill_value=0)

# Plot the original, smoothed, and upscaled error logs
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(
    x=error_logs_over_time.index, 
    y=error_logs_over_time.values, 
    mode='lines+markers', 
    name='Original Error Logs',
    line=dict(color='firebrick', width=2)
))
fig.add_trace(go.Scatter(
    x=error_logs_smoothed.index, 
    y=error_logs_smoothed.values, 
    mode='lines', 
    name='Smoothed Error Logs (Rolling Avg)',
    line=dict(color='blue', width=2, dash='dash')
))
fig.add_trace(go.Scatter(
    x=combined_error_logs_over_time.index, 
    y=combined_error_logs_over_time.values, 
    mode='lines', 
    name='Upscaled Error Logs (Synthetic)',
    line=dict(color='green', width=2, dash='dot')
))
fig.update_layout(
    # title=='Original, Smoothed, and Upscaled Error Logs',
    xaxis_title='Time',
    yaxis_title='Number of Errors',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Use cumulative sum to smooth data over time
c_total_logs_per_day = new_df.resample('D').size()
c_error_logs_over_time = error_logs.resample('D').size()
error_rate = (c_error_logs_over_time / c_total_logs_per_day).fillna(0) * 100  # Convert to percentage
error_logs_cumulative = c_error_logs_over_time.cumsum()

# Plot cumulative errors over time
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=error_logs_cumulative.index, 
    y=error_logs_cumulative.values, 
    mode='lines+markers', 
    name='Cumulative Errors',
    line=dict(color='firebrick', width=2)
))
fig.update_layout(
    # title=='Cumulative Errors Over Time',
    xaxis_title='Time',
    yaxis_title='Cumulative Number of Errors',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Plot different types of errors over time using Plotly with a logarithmic scale
fig = make_subplots(rows=1, cols=1)
for error_type in error_types.unique():
    error_logs_filtered = error_logs[error_types == error_type]
    error_logs_over_time = error_logs_filtered.resample('W').size()
    fig.add_trace(go.Scatter(
        x=error_logs_over_time.index, 
        y=error_logs_over_time.values, 
        mode='lines+markers', 
        name=error_type,
        line=dict(width=2)
    ))
fig.update_layout(
    # title=='Errors Over Time by Type (Logarithmic Scale)',
    xaxis_title='Time',
    yaxis_title='Number of Errors (Log Scale)',
    yaxis_type='log',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Plot column chart of error types using Plotly
fig = go.Figure()
fig.add_trace(go.Bar(
    x=error_type_counts.index, 
    y=error_type_counts.values, 
    name='Error Types',
    marker_color='crimson'
))
fig.update_layout(
    # title=='Error Types Count',
    xaxis_title='Error Type',
    yaxis_title='Count',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Plot error rate over time
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=error_rate.index, 
    y=error_rate.values, 
    mode='lines+markers', 
    name='Error Rate Over Time',
    line=dict(color='royalblue', width=2)
))
fig.update_layout(
    # title=='Error Rate Over Time (as % of Total Logs)',
    xaxis_title='Time',
    yaxis_title='Error Rate (%)',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Add trendlines for errors over time (using rolling averages)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=error_logs_over_time.index, 
    y=error_logs_over_time.values, 
    mode='lines', 
    name='Errors Over Time',
    line=dict(color='firebrick', width=2)
))
fig.add_trace(go.Scatter(
    x=error_trend.index, 
    y=error_trend.values, 
    mode='lines', 
    name='Error Trend (6-day avg)',
    line=dict(color='blue', width=2, dash='dash')
))
fig.update_layout(
    # title=='Errors Over Time with Trendline',
    xaxis_title='Time',
    yaxis_title='Number of Errors',
    hovermode='x unified',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()

# Plot the distribution of errors by hour
fig = go.Figure()
for i, error_type in enumerate(error_logs_grouped.columns):
    fig.add_trace(go.Bar(
        x=error_logs_grouped.index,
        y=error_logs_grouped[error_type],
        name=error_type,
    ))

fig.update_layout(
    # title=='Distribution of Errors by Hour and Type',
    xaxis_title='Hour of the Day',
    yaxis_title='Number of Errors',
    hovermode='x unified',
    barmode='stack',
    # title=_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont=dict(size=layout_settings['xaxis_tickfont_size']),
    yaxis_tickfont=dict(size=layout_settings['yaxis_tickfont_size']),
    legend_font=dict(size=layout_settings['legend_font_size']),
    font=dict(family=layout_settings['font_family'])
)
fig.show()
