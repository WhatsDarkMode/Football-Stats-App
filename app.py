"""
Workflow of app:
    1. User opens app
        - Background check that the calculated stats displayed to the user are calculated 
        based on the raw data csv in the folder
    2. User has the option to update the raw data file if necessary 
    3. User can view calculated stats
    4. User can create teams to see the predicted results of different combinations of players

It makes most sense that the stats are not recalculated everytime the app is loaded, if the raw data hasnt changed.
So calculated stats are stored as a csv, a data validation check is run to check that the calculated stats
are from the most up to data csv (based on whether matches are equal).
"""

# Import packages
import os
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for, send_file
from dash import dash, dcc, dash_table, Input, Output, State

# Import files
from dash_app_files import dash_functions, layout
import raw_data_processing
import config

app = Flask(__name__)
app.secret_key = "abc"

# File paths
MATCH_DATA_PATH = config.MATCH_DATA_PATH
PLAYER_KEYS_PATH = config.PLAYER_KEYS_PATH
MATCH_COUNT_PATH = config.MATCH_COUNT_PATH
PLAYER_STATS_PATH = config.PLAYER_STATS_PATH

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/')

dash_app.layout = layout.create_dashboard_tabs()

# Routes

@app.route('/')
def index():
    return redirect(url_for('stats'))

@app.route('/stats')
def stats():
    if not os.path.exists(PLAYER_STATS_PATH):
        return redirect(url_for('upload_data'))
    
    player_stats_df = pd.read_csv(PLAYER_STATS_PATH)
    return layout.stats_tab_layout(player_stats_df)

@app.route('/recalculate-stats', methods=['POST'])
def recalculate_stats():
    # Process raw match_data
    player_records = raw_data_processing.process_match_data(MATCH_DATA_PATH, MATCH_COUNT_PATH)
    
    # Calculate player stats
    calculated_player_stats = raw_data_processing.calculate_player_stats(player_records)
    
    # Create data frame from player stats
    player_stats_df = raw_data_processing.create_player_stats_df(calculated_player_stats, PLAYER_KEYS_PATH)
    
    # Save player stats dataframe
    raw_data_processing.save_player_stats_df(player_stats_df, PLAYER_STATS_PATH)

    return redirect(url_for('stats'))

@app.route('/download-stats')
def download_stats():
    if os.path.exists(PLAYER_STATS_PATH):
        return send_file(PLAYER_STATS_PATH, as_attachment=True)
    else:
        return "Stats file not found.", 404

@app.route('/upload_data')
def upload_data():
    return layout.upload_tab_layout

# Callbacks

@dash_app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
)
def render_tab_content(selected_tab):
    if selected_tab == 'stats':
        return stats()
    elif selected_tab == 'match_prediction':
        return #prediction tab layout
    elif selected_tab == 'upload_data':
        return upload_data()

@dash_app.callback(
    Output('validation-alert', 'is_open'),
    Output('validation-alert', 'children'),
    Output('validation-alert', 'color'),
    Input('app-load-trigger', 'data'),
    Input('match-data-path', 'data'),
    Input('match-count-path', 'data')
)
def validate_data_on_app_initialisation(data_trigger, match_data_path, match_count_path):
    return dash_functions.app_initialisation_validate_data_check(data_trigger, match_data_path, match_count_path)

@dash_app.callback(
    Output('upload-status-match', 'children'),
    Input('upload-match', 'contents'),
    State('upload-match', 'filename')
)
def upload_match_data(contents, filename):
    if contents is None:
        return "No file uploaded."
    return dash_functions.handle_match_data_upload(filename, contents)
        
@dash_app.callback(
    Output('upload-status-players', 'children'),
    Input('upload-players', 'contents'),
    State('upload-players', 'filename')
)
def upload_player_keys(contents, filename):
    if contents is None:
        return "No file uploaded."
    return dash_functions.handle_player_keys_upload(filename, contents)

context = config.SSL_CONTEXT

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, ssl_context = context)


## 31DEC24 SLS: Next step is to double-check that the tabs are coded how i imagine, e.g. not re-processing everytime etc. 
# 1. Move ml_data_set and player key files over

# 3. Push to Git
# 4. Trial run the app
# 5. Fix any bugs with the app
# 6. Improve the HTML files of the app
# 7. Further improve the stats functionality via duo, trio, quad stats.
# 8. Implement the display of extra stats (duos/trios etc, form, nemesis higlighter?)
# 9. Once fully functional, and operational try implement a prediction tab. 