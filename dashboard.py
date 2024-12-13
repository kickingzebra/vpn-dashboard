import dash
from dash import html, dcc
import plotly.graph_objects as go
from VPNmonitor import VPNMonitor

# Initialize the VPN monitor
vpn_monitor = VPNMonitor(use_mock=True)  # Set to False when using real AWS

# Initialize Dash app
app = dash.Dash(__name__)

# App layout remains the same as before
app.layout = html.Div([
    html.H1('VPN Monitor Dashboard (Test Mode)',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    html.Div([
        html.H2('VPN Status Overview',
                style={'color': '#34495e', 'marginBottom': 20}),
        html.Div(id='vpn-status-table'),
        dcc.Interval(
            id='interval-component',
            interval=5000,
            n_intervals=0
        )
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),

    html.Div([
        html.H2('VPN Metrics',
                style={'color': '#34495e', 'marginBottom': 20}),
        html.Div(id='vpn-metrics-charts')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'})
])


@app.callback(
    dash.Output('vpn-status-table', 'children'),
    dash.Input('interval-component', 'n_intervals')
)
def update_status(n):
    try:
        df = vpn_monitor.get_vpn_status()
        return html.Table(
            [html.Tr([html.Th(col, style={'backgroundColor': '#34495e',
                                          'color': 'white',
                                          'padding': '12px',
                                          'textAlign': 'left'})
                      for col in df.columns])] +
            [html.Tr([
                html.Td(df.iloc[i][col],
                        style={'padding': '12px',
                               'backgroundColor': '#ffffff',
                               'color': '#2c3e50' if col != 'State' else
                               '#27ae60' if df.iloc[i][col] == 'available' else
                               '#e74c3c'})
                for col in df.columns
            ]) for i in range(len(df))],
            style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '20px'}
        )
    except Exception as e:
        return html.Div(f"Error fetching VPN status: {str(e)}")


@app.callback(
    dash.Output('vpn-metrics-charts', 'children'),
    dash.Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    try:
        df = vpn_monitor.get_vpn_status()
        charts = []

        for vpn_id in df['VPN ID']:
            metrics_df = vpn_monitor.get_vpn_metrics(vpn_id)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=metrics_df['Timestamp'],
                y=metrics_df['TunnelState'],
                mode='lines+markers',
                name=f'Tunnel State',
                line=dict(color='#2980b9'),
                marker=dict(size=8)
            ))

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
    app.run_server(debug=True)

# Create figures
revenue_chart = px.line(df, x='Month', y='Revenue', title='Monthly Revenue')
expense_chart = px.line(df, x='Month', y='Expenses', title='Monthly Expenses')
comparison_chart = px.bar(df, x='Month', y=['Revenue', 'Expenses'], barmode='group', title='Revenue vs Expenses')

# App layout
app.layout = html.Div([
    html.H1('Business Performance Dashboard'),

    dcc.Graph(figure=revenue_chart),
    dcc.Graph(figure=expense_chart),
    dcc.Graph(figure=comparison_chart)
])

if __name__ == '__main__':
    app.run_server(debug=True)# Create a virtual environment

