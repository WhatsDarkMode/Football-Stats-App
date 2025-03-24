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

# ----------- Import packages -----------
import os
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for, send_file, jsonify
# import matplotlib.pyplot as plt
import io
import base64
import json
# for development using styles.css
from datetime import datetime

# ----------- Import files -----------
import functions
import display
import raw_data_processing
import data_visualisations
import config
from error_classes import MissingFileError, JsonLoadError, EmptyFileError, DataProcessingError

app = Flask(__name__)
app.secret_key = "abc"

# ----------- Global variable -----------
initialised = False
player_stats_df = pd.DataFrame()
player_form_dict = {}
player_keys_dict = {}
initialisation_errors = []

# ----------- File paths -----------
MATCH_DATA_PATH = config.MATCH_DATA_PATH
PLAYER_KEYS_PATH = config.PLAYER_KEYS_PATH
MATCH_COUNT_PATH = config.MATCH_COUNT_PATH
PLAYER_STATS_PATH = config.PLAYER_STATS_PATH
PLAYER_FORM_DICT_PATH = config.PLAYER_FORM_DICT_PATH


# ----------- Routes -----------
with app.app_context():
    try:
        if not initialised:
            try:
                file_statuses = {
                    "match_data": functions.csv_file_checker(MATCH_DATA_PATH),
                    "player_keys": functions.csv_file_checker(PLAYER_KEYS_PATH),
                    "player_stats": functions.csv_file_checker(PLAYER_STATS_PATH),
                    "player_form_dict": functions.json_file_checker(PLAYER_FORM_DICT_PATH)
                }
            except MissingFileError as e:
                initialisation_errors.append(str(e))

            if file_statuses['player_stats']['has_data'] and file_statuses['player_form_dict']['has_data']:
                try:
                    player_stats_df = pd.read_csv(PLAYER_STATS_PATH)
                    with open(PLAYER_FORM_DICT_PATH, 'r') as file:
                        player_form_dict = json.load(file)

                    if isinstance(player_stats_df, pd.DataFrame) and player_stats_df.empty:
                        if file_statuses['match_data']['has_data'] and file_statuses['player_keys']['has_data']:
                            try:
                                player_stats_df, player_form_dict = raw_data_processing.cs_player_stats_player_form(MATCH_DATA_PATH, MATCH_COUNT_PATH, PLAYER_KEYS_PATH, PLAYER_STATS_PATH, PLAYER_FORM_DICT_PATH)
                            except DataProcessingError as e:
                                initialisation_errors.append(str(e))
                        else:
                            initialisation_errors.append("match_data or player_keys file is empty")
                
                except (pd.errors.EmptyDataError, FileNotFoundError) as e:
                    initialisation_errors.append(f"Error loading player_stats or player_form files: {e}")
                    
    except Exception as e:
        initialisation_errors.append(f"Unexpected error initializing app: {e}")


@app.route('/')
def home():
    return render_template('home.html', timestamp=datetime.now().timestamp(), errors=initialisation_errors)


@app.route('/stats')
def stats():
    global player_stats_df, player_keys_dict

    if os.path.exists(PLAYER_KEYS_PATH):
        player_keys_df = pd.read_csv(PLAYER_KEYS_PATH)
        player_keys_dict = player_keys_df.set_index('player_id')['player_name'].to_dict()

    if player_stats_df.empty:
        response = display.response("error", "Player stats could not be loaded or created. Please ensure the required files are uploaded and try again.")  
        return render_template('stats.html', player_keys_dict=player_keys_dict, response=response)

    # Generate example Form heatmap graph
    default_player_ids = list(player_form_dict.keys())[:4]
    form_window = 10
    plotly_heatmap = data_visualisations.form_heatmap(default_player_ids, form_window, player_form_dict, player_keys_dict)
    
    # Generate goal difference scatter plot
    plotly_scatter = data_visualisations.goal_diff_scatter_plot(player_stats_df)
    
    # Generate W/D/L stacked bar chat
    plotly_bargraph = data_visualisations.results_bar_graph(player_stats_df)

    response = display.response("success", "Great success", player_stats_df.to_dict())  
    return render_template('stats.html', 
                        player_keys_dict=player_keys_dict,
                        player_stats_df=player_stats_df,
                        plotly_heatmap=plotly_heatmap, 
                        plotly_scatter=plotly_scatter, 
                        plotly_bargraph=plotly_bargraph, 
                        response=response)


@app.route('/generate_form_heatmap', methods=['POST'])
def generate_form_heatmap():
    global player_form_dict, player_keys_dict

    player_ids = request.form.getlist('player_ids')
    form_window = int(request.form['form_window'])

    form_heatmap = data_visualisations.form_heatmap(player_ids, form_window, player_form_dict, player_keys_dict)

    return jsonify({"status": "success", "form_heatmap_json": form_heatmap})    


@app.route('/stats/recalculate')
def recalculate_player_stats():
    global player_stats_df, player_form_dict
    player_stats_df, player_form_dict = raw_data_processing.cs_player_stats_player_form(MATCH_DATA_PATH, MATCH_COUNT_PATH, PLAYER_KEYS_PATH, PLAYER_STATS_PATH, PLAYER_FORM_DICT_PATH)
    return redirect(url_for('stats'))


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return display.response("error", "file upload error")
        
        file = request.files['file']
        file_type = request.form.get('file_type')

        upload_result = functions.upload(file, file_type, MATCH_DATA_PATH, PLAYER_KEYS_PATH)

        return render_template('upload.html', response=upload_result)
    
    except Exception as e:
        error_message = f"An error occurred during file upload: {str(e)}"
        return render_template('upload.html', response=display.reponse("error", error_message))

context = config.SSL_CONTEXT

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, ssl_context = context)
    







# 25FEB25
# 1. Fix re-calculate display and double check functionality (it should be above/next to player stats)
# 2. Make upload button style match stats
# 3. Add some filler content on home page
# 4. Upload to git
# 5. Comb through code to clean it up and remove unecessary files
# 6. Explore predition functionality