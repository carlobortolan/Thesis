'''
gRPC vs REST API Comparison
'''

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

rest_data = pd.read_csv('data/summary_150_10_10000.csv')
grpc_data = pd.read_csv('data/summary_150_10_10000_grpc.csv')

rest_data['timeStamp'] = pd.to_datetime(rest_data['timeStamp'], unit='ms')
grpc_data['timeStamp'] = pd.to_datetime(grpc_data['timeStamp'], unit='ms')

# Calculate success rates
rest_success_rate = rest_data['success'].mean() * 100
grpc_success_rate = grpc_data['success'].mean() * 100

# Normalize time to start from zero
rest_data['normalizedTime'] = (rest_data['timeStamp'] - rest_data['timeStamp'].min()).dt.total_seconds() / 60  # in minutes
grpc_data['normalizedTime'] = (grpc_data['timeStamp'] - grpc_data['timeStamp'].min()).dt.total_seconds() / 60  # in minutes

# Throughput analysis: group by normalized minute
rest_data['normalizedMinute'] = rest_data['normalizedTime'].astype(int)
grpc_data['normalizedMinute'] = grpc_data['normalizedTime'].astype(int)

rest_throughput = rest_data.groupby('normalizedMinute').size()
grpc_throughput = grpc_data.groupby('normalizedMinute').size()

# Error rate calculation: group by normalized minute
rest_errors = rest_data[~rest_data['success']].groupby('normalizedMinute').size()
grpc_errors = grpc_data[~grpc_data['success']].groupby('normalizedMinute').size()

# Calculate error rate as percentage
rest_error_rate = (rest_errors / rest_throughput) * 100
grpc_error_rate = (grpc_errors / grpc_throughput) * 100

# Remove outliers using IQR method
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    return df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]

rest_data_clean = remove_outliers(rest_data, 'elapsed')
grpc_data_clean = remove_outliers(grpc_data, 'elapsed')

# Filter out rows where the response time is 0ms
rest_data_filtered = rest_data_clean[rest_data_clean['elapsed'] > 0]
grpc_data_filtered = grpc_data_clean[grpc_data_clean['elapsed'] > 0]

# Visualization 1: Box plot comparing Response Time (Elapsed)
fig1 = go.Figure()

fig1.add_trace(go.Box(y=rest_data['elapsed'], name='REST API', boxmean='sd'))
fig1.add_trace(go.Box(y=grpc_data['elapsed'], name='gRPC API', boxmean='sd'))

fig1.update_layout(
    # title="Response Time Comparison (Elapsed Time)",
    yaxis_title="Elapsed Time (ms)",
    xaxis_title="API Type",
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

# Visualization 2: Line plot of throughput over normalized time
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=rest_throughput.index, y=rest_throughput, mode='lines', name='REST API'))
fig2.add_trace(go.Scatter(x=grpc_throughput.index, y=grpc_throughput, mode='lines', name='gRPC API'))

fig2.update_layout(
    # title="Throughput Over Normalized Time",
    xaxis_title="Normalized Time (minutes)",
    yaxis_title="Number of Requests",
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

# Visualization 3: Bar plot of Success Rate
fig3 = go.Figure()

fig3.add_trace(go.Bar(x=['REST API'], y=[rest_success_rate], name='REST API'))
fig3.add_trace(go.Bar(x=['gRPC API'], y=[grpc_success_rate], name='gRPC API'))

fig3.update_layout(
    # title="Success Rate Comparison",
    yaxis_title="Success Rate (%)",
    xaxis_title="API Type",
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

# Visualization 4: Bar plot for Bytes Sent and Received
fig4 = go.Figure()

fig4.add_trace(go.Bar(x=['REST API'], y=[rest_data['bytes'].sum()], name='Bytes Received (REST)'))
fig4.add_trace(go.Bar(x=['gRPC API'], y=[grpc_data['bytes'].sum()], name='Bytes Received (gRPC)'))

fig4.add_trace(go.Bar(x=['REST API'], y=[rest_data['sentBytes'].sum()], name='Bytes Sent (REST)'))
fig4.add_trace(go.Bar(x=['gRPC API'], y=[grpc_data['sentBytes'].sum()], name='Bytes Sent (gRPC)'))

fig4.update_layout(
    # title="Bytes Sent and Received Comparison",
    yaxis_title="Total Bytes",
    barmode='group',
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

# Visualization 5: Histogram of Response Time Distribution
fig5 = go.Figure()
bin_size = 1

fig5.add_trace(go.Histogram(x=rest_data_filtered['elapsed'], name='REST API', opacity=0.75, xbins=dict(size=bin_size)))
fig5.add_trace(go.Histogram(x=grpc_data_filtered['elapsed'], name='gRPC API', opacity=0.75, xbins=dict(size=bin_size)))

fig5.update_layout(
    # title="Response Time Distribution",
    xaxis_title="Elapsed Time (ms)",
    yaxis_title="Frequency",
    barmode='overlay',
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

fig5.update_traces(opacity=0.75)

# Visualization 6: Line plot of Error Rate over time
fig6 = go.Figure()

fig6.add_trace(go.Scatter(x=rest_error_rate.index, y=rest_error_rate, mode='lines', name='REST API Error Rate'))
fig6.add_trace(go.Scatter(x=grpc_error_rate.index, y=grpc_error_rate, mode='lines', name='gRPC API Error Rate'))

fig6.update_layout(
    # title="Error Rate Over Time",
    xaxis_title="Normalized Time (minutes)",
    yaxis_title="Error Rate (%)",
    title_font_size=layout_settings['title_font_size'],
    xaxis_title_font_size=layout_settings['xaxis_title_font_size'],
    yaxis_title_font_size=layout_settings['yaxis_title_font_size'],
    xaxis_tickfont_size=layout_settings['xaxis_tickfont_size'],
    yaxis_tickfont_size=layout_settings['yaxis_tickfont_size'],
    legend_font_size=layout_settings['legend_font_size'],
    font=dict(family=layout_settings['font_family'])
)

fig1.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig6.show()