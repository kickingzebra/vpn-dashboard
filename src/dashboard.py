"""
Enhanced VPN Dashboard
Features comprehensive monitoring of VPN status, performance, and security
"""

from dash import Dash, html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from VPNmonitor import VPNMonitor

# Initialize VPN monitor
vpn_monitor = VPNMonitor(use_mock=True)  # Set to False for real AWS connection

# Initialize Dash app
app = Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1('VPN Monitoring Dashboard',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Active Sessions Section
    html.Div([
        html.H2('Active Sessions',
                style={'color': '#34495e', 'marginBottom': 20}),
        html.Div(id='active-sessions-table'),
        dcc.Graph(id='sessions-map')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
    
    # Performance Metrics Section
    html.Div([
        html.H2('Performance Metrics',
                style={'color': '#34495e', 'marginBottom': 20}),
        dcc.Tabs([
            dcc.Tab(label='Bandwidth', children=[
                dcc.Graph(id='bandwidth-graph')
            ]),
            dcc.Tab(label='Latency', children=[
                dcc.Graph(id='latency-graph')
            ]),
            dcc.Tab(label='Resource Usage', children=[
                dcc.Graph(id='resource-usage-graph')
            ])
        ])
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
    
    # Security Events Section
    html.Div([
        html.H2('Security Events',
                style={'color': '#34495e', 'marginBottom': 20}),
        html.Div(id='security-events-table'),
        dcc.Graph(id='security-events-timeline')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
    
    # Compliance Status Section
    html.Div([
        html.H2('Compliance & Security',
                style={'color': '#34495e', 'marginBottom': 20}),
        html.Div(id='compliance-status')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
    
    # Update interval
    dcc.Interval(
        id='update-interval',
        interval=5000,  # 5 seconds
        n_intervals=0
    )
])

# Callback for active sessions
@app.callback(
    [Output('active-sessions-table', 'children'),
     Output('sessions-map', 'figure')],
    Input('update-interval', 'n_intervals')
)
def update_sessions(n):
    sessions = vpn_monitor.get_active_sessions()
    
    # Create sessions table
    table = html.Table(
        [html.Tr([html.Th(col) for col in ['User', 'IP', 'Duration', 'Location']])] +
        [html.Tr([
            html.Td(session.username),
            html.Td(session.ip_address),
            html.Td(str(session.duration)),
            html.Td(f"{session.location['city']}, {session.location['country']}")
        ]) for session in sessions],
        style={'width': '100%', 'marginBottom': '20px'}
    )
    
    # Create world map
    map_fig = px.scatter_geo(
        pd.DataFrame([s.location for s in sessions]),
        lat='latitude',
        lon='longitude',
        hover_name='city',
        projection='natural earth'
    )
    
    return table, map_fig

# Callback for performance metrics
@app.callback(
    [Output('bandwidth-graph', 'figure'),
     Output('latency-graph', 'figure'),
     Output('resource-usage-graph', 'figure')],
    Input('update-interval', 'n_intervals')
)
def update_performance(n):
    metrics = vpn_monitor.get_performance_metrics()
    
    # Bandwidth graph
    bandwidth_fig = go.Figure()
    bandwidth_fig.add_trace(go.Scatter(
        x=metrics['bandwidth']['timestamps'],
        y=metrics['bandwidth']['inbound'],
        name='Inbound'
    ))
    bandwidth_fig.add_trace(go.Scatter(
        x=metrics['bandwidth']['timestamps'],
        y=metrics['bandwidth']['outbound'],
        name='Outbound'
    ))
    
    # Latency graph
    latency_fig = go.Figure()
    latency_fig.add_trace(go.Scatter(
        x=metrics['latency']['timestamps'],
        y=metrics['latency']['values'],
        name='Latency (ms)'
    ))
    
    # Resource usage graph
    resource_fig = go.Figure()
    resource_fig.add_trace(go.Bar(
        x=['CPU', 'Memory', 'Disk'],
        y=[metrics['resource_utilization']['cpu'],
           metrics['resource_utilization']['memory'],
           metrics['resource_utilization']['disk']],
        name='Usage %'
    ))
    
    return bandwidth_fig, latency_fig, resource_fig

# Callback for security events
@app.callback(
    [Output('security-events-table', 'children'),
     Output('security-events-timeline', 'figure')],
    Input('update-interval', 'n_intervals')
)
def update_security_events(n):
    events = vpn_monitor.get_security_events()
    
    # Create events table
    table = html.Table(
        [html.Tr([html.Th(col) for col in ['Time', 'Event', 'User', 'Details']])] +
        [html.Tr([
            html.Td(event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')),
            html.Td(event['event_type']),
            html.Td(event['username']),
            html.Td(event['details'])
        ]) for event in events],
        style={'width': '100%', 'marginBottom': '20px'}
    )
    
    # Create timeline
    timeline_fig = go.Figure()
    timeline_fig.add_trace(go.Scatter(
        x=[e['timestamp'] for e in events],
        y=[e['event_type']
