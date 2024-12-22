"""
VPN Dashboard
A comprehensive monitoring dashboard for VPN connections
Using mock data for development and testing
"""

from dash import Dash, html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from VPNmonitor import VPNMonitor

# Initialize VPN monitor with mock data
vpn_monitor = VPNMonitor(use_mock=True)

# Initialize Dash app
app = Dash(__name__)

# Define the layout with multiple tabs
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('VPN Monitoring Dashboard',
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P('Test Environment - Using Mock Data',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': 20})
    ]),

    # Main content with tabs
    dcc.Tabs([
        # Overview Tab
        dcc.Tab(label='Overview', children=[
            html.Div([
                # Status Summary Cards
                html.Div([
                    html.Div([
                        html.H3('Active Connections'),
                        html.H2(id='active-connections-count'),
                        html.P(id='active-connections-change')
                    ], className='summary-card'),
                    html.Div([
                        html.H3('Current Bandwidth'),
                        html.H2(id='current-bandwidth'),
                        html.P(id='bandwidth-trend')
                    ], className='summary-card'),
                    html.Div([
                        html.H3('System Health'),
                        html.H2(id='system-health-status'),
                        html.P(id='system-health-detail')
                    ], className='summary-card')
                ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0'})
            ])
        ]),

        # Active Sessions Tab
        dcc.Tab(label='Active Sessions', children=[
            html.Div([
                html.H2('Current VPN Sessions',
                        style={'color': '#2c3e50', 'marginBottom': 20}),
                html.Div(id='sessions-table'),
                dcc.Graph(id='sessions-map')
            ], style={'padding': '20px'})
        ]),

        # Performance Tab
        dcc.Tab(label='Performance', children=[
            html.Div([
                html.H2('Performance Metrics',
                        style={'color': '#2c3e50', 'marginBottom': 20}),
                dcc.Graph(id='bandwidth-graph'),
                dcc.Graph(id='latency-graph'),
                dcc.Graph(id='resource-usage-graph')
            ], style={'padding': '20px'})
        ]),

        # Security Tab
        dcc.Tab(label='Security', children=[
            html.Div([
                html.H2('Security Events',
                        style={'color': '#2c3e50', 'marginBottom': 20}),
                html.Div(id='security-alerts'),
                dcc.Graph(id='security-events-timeline')
            ], style={'padding': '20px'})
        ])
    ]),

    # Update interval
    dcc.Interval(
        id='update-interval',
        interval=5000,  # 5 seconds
        n_intervals=0
    ),

    # CSS styling
    html.Style('''
        .summary-card {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 30%;
            text-align: center;
        }
        .alert {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .alert-warning {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
        }
        .alert-danger {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
    ''')
])

# Callback for overview cards
@app.callback(
    [Output('active-connections-count', 'children'),
     Output('active-connections-change', 'children'),
     Output('current-bandwidth', 'children'),
     Output('bandwidth-trend', 'children'),
     Output('system-health-status', 'children'),
     Output('system-health-detail', 'children')],
    [Input('update-interval', 'n_intervals')]
)
def update_overview_cards(n):
    # Mock data for testing
    return (
        "12",  # Active connections
        "↑ 2 from last hour",  # Connection change
        "1.2 GB/s",  # Current bandwidth
        "↑ 15% from average",  # Bandwidth trend
        "Good",  # System health
        "All systems operational"  # Health detail
    )

# Callback for sessions table and map
@app.callback(
    [Output('sessions-table', 'children'),
     Output('sessions-map', 'figure')],
    [Input('update-interval', 'n_intervals')]
)
def update_sessions(n):
    # Mock session data
    mock_sessions = pd.DataFrame({
        'User': ['user1', 'user2', 'user3'],
        'IP': ['192.168.1.1', '192.168.1.2', '192.168.1.3'],
        'Location': ['New York', 'London', 'Tokyo'],
        'Duration': ['2h 15m', '45m', '1h 30m'],
        'Status': ['Connected', 'Connected', 'Connected']
    })

    # Create table
    table = html.Table(
        [html.Tr([html.Th(col) for col in mock_sessions.columns])] +
        [html.Tr([html.Td(mock_sessions.iloc[i][col]) for col in mock_sessions.columns])
         for i in range(len(mock_sessions))],
        style={'width': '100%', 'marginBottom': '20px'}
    )

    # Create map (using mock coordinates)
    map_data = pd.DataFrame({
        'city': ['New York', 'London', 'Tokyo'],
        'lat': [40.7128, 51.5074, 35.6762],
        'lon': [-74.0060, -0.1278, 139.6503]
    })

    map_fig = px.scatter_mapbox(
        map_data,
        lat='lat',
        lon='lon',
        hover_name='city',
        zoom=1
    )

    map_fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return table, map_fig

# Callback for performance graphs
@app.callback(
    [Output('bandwidth-graph', 'figure'),
     Output('latency-graph', 'figure'),
     Output('resource-usage-graph', 'figure')],
    [Input('update-interval', 'n_intervals')]
)
def update_performance_graphs(n):
    # Mock time series data
    times = pd.date_range(start='2024-01-01', periods=24, freq='H')
    
    # Bandwidth graph
    bandwidth_fig = go.Figure()
    bandwidth_fig.add_trace(go.Scatter(
        x=times,
        y=[random.uniform(50, 150) for _ in range(24)],
        name='Inbound',
        line=dict(color='#2ecc71')
    ))
    bandwidth_fig.add_trace(go.Scatter(
        x=times,
        y=[random.uniform(30, 100) for _ in range(24)],
        name='Outbound',
        line=dict(color='#3498db')
    ))
    bandwidth_fig.update_layout(
        title='Bandwidth Usage (Last 24 Hours)',
        xaxis_title='Time',
        yaxis_title='MB/s'
    )

    # Latency graph
    latency_fig = go.Figure()
    latency_fig.add_trace(go.Scatter(
        x=times,
        y=[random.uniform(10, 50) for _ in range(24)],
        name='Latency',
        line=dict(color='#e74c3c')
    ))
    latency_fig.update_layout(
        title='Connection Latency',
        xaxis_title='Time',
        yaxis_title='ms'
    )

    # Resource usage graph
    resources = ['CPU', 'Memory', 'Disk', 'Network']
    usage_fig = go.Figure(data=[
        go.Bar(
            x=resources,
            y=[random.uniform(20, 80) for _ in range(4)],
            marker_color='#9b59b6'
        )
    ])
    usage_fig.update_layout(
        title='Resource Utilization',
        yaxis_title='Percentage Used'
    )

    return bandwidth_fig, latency_fig, usage_fig

# Callback for security events
@app.callback(
    [Output('security-alerts', 'children'),
     Output('security-events-timeline', 'figure')],
    [Input('update-interval', 'n_intervals')]
)
def update_security_events(n):
    # Mock security alerts
    alerts = html.Div([
        html.Div(
            "Failed login attempt from unauthorized IP (192.168.1.100)",
            className='alert alert-warning'
        ),
        html.Div(
            "Multiple connection attempts detected from single IP",
            className='alert alert-danger'
        )
    ])

    # Mock security events timeline
    times = pd.date_range(start='2024-01-01', periods=10, freq='H')
    events = ['Login Success', 'Config Change', 'Login Failure', 'VPN Start',
              'Login Success', 'Login Success', 'Config Change', 'Login Failure',
              'VPN Stop', 'VPN Start']
    
    timeline_fig = go.Figure(data=[
        go.Scatter(
            x=times,
            y=events,
            mode='markers+text',
            marker=dict(
                size=12,
                color=['green' if 'Success' in e else 'red' if 'Failure' in e else 'blue'
                       for e in events]
            ),
            text=events,
            textposition="middle right"
        )
    ])
    
    timeline_fig.update_layout(
        title='Security Events Timeline',
        showlegend=False,
        height=400
    )

    return alerts, timeline_fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)


