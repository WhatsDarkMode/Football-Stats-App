from dash import dcc, html, dash_table
import pandas as pd

def create_dashboard_tabs():
    """
    Creates and returns the layout for a dashboard with tabs.
    """
    layout = html.Div(
        children=[
            # Tabs for navigation
            dcc.Tabs(
                id='tabs',  # Unique ID for the tabs
                value='view_stats',  # Default active tab
                children=[
                    dcc.Tab(label='View Statistics', value='stats'),
                    dcc.Tab(label='Match Prediction', value='match_prediction'),
                    dcc.Tab(label='Upload Data', value='upload_data'),
                ]
            ),
            # Store for triggering data validation on app load
            dcc.Store(id='app-load-trigger', data={'loaded': True}),
            # Store file paths to raw data and match count
            dcc.Store(id='raw-data-path', data='C:\My Documents\football\data\raw\match_data.csv'),
            dcc.Store(id='match-count-path', data='C:\My Documents\football\data\calculated\match_count.txt'),

            # Alert for data validation
            dcc.Alert(
                id='validation-alert',
                is_open=False, # Initially hidden
                dismissable=True, # Allows user to close it
                duration = 5000, # Auto-dismiss after 5 seconds
                style = {"marginBottom": "20px"}
            ),

            # Content area that updates based on the selected tab
            html.Div(
                id='tabs-content',  # Placeholder for dynamic content
                style={"padding": "20px"}
            )
        ],
        style={"fontFamily": "Arial, sans-serif", "padding": "10px"}
    )

    return layout

def upload_tab_layout():
    """
    Returns the layout for the tab to upload a new match data or player keys CSV file.
    """
    return html.Div([
        html.H1("Upload Match Data or Player Keys", style={'textAlign': 'center'}),
        
        # Section for uploading match data
        html.Div([
            html.H2("Upload Match Data", style={'textAlign': 'left'}),
            dcc.Upload(
                id='upload-match',
                children=html.Button('Upload Match Data', style={"margin": "10px"}),
            ),
            html.Div(id='upload-status-match', style={'margin-top': '10px'}),
        ], style={"margin-bottom": "20px"}),

        # Section for uploading player keys
        html.Div([
            html.H2("Upload Player Keys", style={'textAlign': 'left'}),
            dcc.Upload(
                id='upload-players',
                children=html.Button('Upload Player Keys Data', style={"margin": "10px"}),
            ),
            html.Div(id='upload-status-players', style={'margin-top': '10px'}),
        ])
    ])

def stats_tab_layout(player_stats_df):
    """
    Returns the layout for the stats tab.
    """
    return html.Div([
        html.H1("Player Stats", style={'textAlign': 'center'}),

        # Button to recalculate player stats
        html.Div([
            html.Form(action="/recalculate-stats", method="POST"),
            html.Button('Recalculate Player Stats', className='btn btn-primary mb-3', type="submit"),
        ], style={'textAlign': 'center'}),

        # Download stats button
        html.Div([
            html.A('Download Stats', href="/download-stats", className='btn btn-secondary mb-3')
        ], style={'textAlign': 'center'}),

        # Display the player stats table
        html.Div([
            dash_table.DataTable(
                id='player-stats-table',
                columns=[{'name': col, 'id': col} for col in player_stats_df.columns],
                data=player_stats_df.to_dict('records'),
                style_table={'overflowX': 'auto', # Make table horizontally scrollable
                             'overflowY': 'auto'},  # Make table vertically scrollable
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
            ),
        ], style={'margin-top': '20px'})
    ])