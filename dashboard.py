"""
VPN Dashboard Application
------------------------
This application provides a web-based dashboard for monitoring VPN connections.
It uses Dash for the web interface and runs inside a Docker container.

Configuration:
- Internal container port: 8050
- External access port: 4000
- Access URL: http://localhost:4000

Docker Commands:
    Build: docker build -t vpn-dashboard .
    Run:   docker run -p 4000:8050 vpn-dashboard

Author: [Your Name]
Date: December 2024
"""

from dash import Dash, html, dcc  # Import Dash components
import dash  # For callbacks
import plotly.graph_objects as go  # For creating graphs
from VPNmonitor import VPNMonitor  # Custom VPN monitoring class

# Initialize the VPN monitor with mock data for testing
# Set use_mock=False when connecting to real AWS VPN
vpn_monitor = VPNMonitor(use_mock=True)

# Initialize the Dash application
app = Dash(__name__)

# Define the dashboard layout
app.layout = html.Div([
    # Dashboard Header
    html.H1('VPN Monitor Dashboard (Test Mode)',
            style={'textAlign': 'center',
                   'color': '#2c3e50',
                   'marginBottom': 30}),

    # VPN Status Section
    html.Div([
        html.H2('VPN Status Overview',
                style={'color': '#34495e',
                       'marginBottom': 20}),
        # Container for the status table
        html.Div(id='vpn-status-table'),
        # Interval component for automatic updates
        dcc.Interval(
            id='interval-component',
            interval=5000,  # Update every 5 seconds
            n_intervals=0
        )
    ], style={'margin': '20px',
              'padding': '20px',
              'backgroundColor': '#f8f9fa',
              'borderRadius': '5px'}),

    # VPN Metrics Section
    html.Div([
        html.H2('VPN Metrics',
                style={'color': '#34495e',
                       'marginBottom': 20}),
        # Container for metrics charts
        html.Div(id='vpn-metrics-charts')
    ], style={'margin': '20px',
              'padding': '20px',
              'backgroundColor': '#f8f9fa',
              'borderRadius': '5px'})
])


@app.callback(
    dash.Output('vpn-status-table', 'children'),
    dash.Input('interval-component', 'n_intervals')
)
def update_status(n):
    """
    Callback to update the VPN status table.
    Updates every time the interval timer triggers.

    Args:
        n (int): Number of intervals elapsed (not used but required by Dash)

    Returns:
        html.Table: Formatted table showing VPN status
    """
    try:
        # Get current VPN status
        df = vpn_monitor.get_vpn_status()

        # Create and return formatted table
        return html.Table(
            # Table Header
            [html.Tr([html.Th(col,
                              style={'backgroundColor': '#34495e',
                                     'color': 'white',
                                     'padding': '12px',
                                     'textAlign': 'left'})
                      for col in df.columns])] +
            # Table Body
            [html.Tr([
                html.Td(df.iloc[i][col],
                        style={'padding': '12px',
                               'backgroundColor': '#ffffff',
                               # Color coding for state column
                               'color': '#2c3e50' if col != 'State' else
                               '#27ae60' if df.iloc[i][col] == 'available' else
                               '#e74c3c'})
                for col in df.columns
            ]) for i in range(len(df))],
            style={'width': '100%',
                   'borderCollapse': 'collapse',
                   'marginTop': '20px'}
        )
    except Exception as e:
        return html.Div(f"Error fetching VPN status: {str(e)}")


@app.callback(
    dash.Output('vpn-metrics-charts', 'children'),
    dash.Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    """
    Callback to update the VPN metrics charts.
    Creates a line chart for each VPN connection showing its tunnel state.

    Args:
        n (int): Number of intervals elapsed (not used but required by Dash)

    Returns:
        html.Div: Container with charts for each VPN connection
    """
    try:
        # Get VPN status to know which VPNs to chart
        df = vpn_monitor.get_vpn_status()
        charts = []

        # Create a chart for each VPN
        for vpn_id in df['VPN ID']:
            # Get metrics for this VPN
            metrics_df = vpn_monitor.get_vpn_metrics(vpn_id)

            # Create figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=metrics_df['Timestamp'],
                y=metrics_df['TunnelState'],
                mode='lines+markers',
                name='Tunnel State',
                line=dict(color='#2980b9'),
                marker=dict(size=8)
            ))

            # Update layout
            fig.update_layout(
                title=f'VPN Tunnel State - {vpn_id}',
                xaxis_title='Time',
                yaxis_title='State',
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(
                    tickmode='array',
                    ticktext=['Down', 'Up'],
                    tickvals=[0, 1],
                    gridcolor='#f0f0f0'
                ),
                xaxis=dict(gridcolor='#f0f0f0')
            )

            charts.append(dcc.Graph(figure=fig))

        return html.Div(charts)
    except Exception as e:
        return html.Div(f"Error fetching VPN metrics: {str(e)}")


if __name__ == '__main__':
    # Start the Dash server
    app.run_server(
        debug=True,  # Enable debug mode for development
        host='0.0.0.0',  # Listen on all network interfaces (required for Docker)
        port=8050  # Port inside the container
    )

