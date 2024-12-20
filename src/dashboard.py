# Add to your imports
from dash import html, dcc, callback_context
import plotly.graph_objects as go
from datetime import datetime, timedelta
from test_monitor import TestMonitor

# Initialize test monitor
test_monitor = TestMonitor()

# Add to your layout
app.layout = html.Div([
    # ... existing layout ...

    # Add tab container
    dcc.Tabs([
        dcc.Tab(label='VPN Status', children=[
            # Move your existing status content here
        ]),

        dcc.Tab(label='Test Results', children=[
            html.Div([
                html.H2('VPN Test Results',
                        style={'color': '#34495e', 'marginBottom': 20}),

                # Test Summary Cards
                html.Div([
                    html.Div(id='test-summary-cards',
                            className='summary-cards'),

                    # Time Range Selector
                    dcc.Dropdown(
                        id='time-range-selector',
                        options=[
                            {'label': 'Last 24 Hours', 'value': 24},
                            {'label': 'Last 7 Days', 'value': 168},
                            {'label': 'Last 30 Days', 'value': 720}
                        ],
                        value=24,
                        style={'width': '200px', 'marginBottom': '20px'}
                    ),

                    # Test Results Graph
                    dcc.Graph(id='test-results-graph'),

                    # Detailed Test Results Table
                    html.Div(id='test-results-table')
                ])
            ])
        ])
    ])
])

# Add callbacks for test results
@app.callback(
    [Output('test-summary-cards', 'children'),
     Output('test-results-graph', 'figure'),
     Output('test-results-table', 'children')],
    [Input('time-range-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_test_results(hours, n):
    """Update all test result components"""
    # Get test data
    summary = test_monitor.get_test_summary()
    recent_results = test_monitor.get_recent_results(hours=hours)

    # Create summary cards
    summary_cards = []
    for test_type, stats in summary.items():
        card = html.Div([
            html.H3(test_type.replace('_', ' ').title()),
            html.P(f"Success Rate: {stats['success_rate']:.1f}%"),
            html.P(f"Total Tests: {stats['total']}"),
            html.P(f"Passed: {stats['passed']}"),
            html.P(f"Failed: {stats['failed']}")
        ], className='summary-card')
        summary_cards.append(card)

    # Create timeline graph
    fig = go.Figure()
    for test_type, results in recent_results.items():
        timestamps = [datetime.fromisoformat(r['timestamp']) for r in results]
        statuses = [1 if r['status'] == 'passed' else 0 for r in results]

        fig.add_trace(go.Scatter(
            x=timestamps,
            y=statuses,
            mode='markers',
            name=test_type.replace('_', ' ').title(),
            marker=dict(
                size=10,
                symbol='circle',
                color=['green' if s == 1 else 'red' for s in statuses]
            )
        ))

    fig.update_layout(
        title='Test Results Timeline',
        xaxis_title='Time',
        yaxis=dict(
            tickmode='array',
            ticktext=['Failed', 'Passed'],
            tickvals=[0, 1]
        ),
        plot_bgcolor='white'
    )

    # Create detailed table
    table_header = [
        html.Thead(html.Tr([
            html.Th('Timestamp'),
            html.Th('Test Type'),
            html.Th('Test Name'),
            html.Th('Status'),
            html.Th('Details')
        ]))
    ]

    rows = []
    for test_type, results in recent_results.items():
        for result in results:
            row = html.Tr([
                html.Td(datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')),
                html.Td(test_type.replace('_', ' ').title()),
                html.Td(result['test_name']),
                html.Td(result['status'].title()),
                html.Td(str(result['details']))
            ])
            rows.append(row)

    table_body = [html.Tbody(rows)]
    table = html.Table(table_header + table_body)

    return summary_cards, fig, table

# Add some CSS for the test results page
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>VPN Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .summary-cards {
                display: flex;
                justify-content: space-around;
                margin-bottom: 20px;
            }
            .summary-card {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                width: 200px;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #34495e;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

