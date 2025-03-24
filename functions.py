import pandas as pd
import json
import base64
import io
import os


from error_classes import MissingFileError, UploadError
from display import response
import raw_data_processing


def response(status, message, data=None):
    response_result = {
        "status": status,
        "message": message
    }
    if data:
        response_result['data'] = data
    
    return response_result


def upload(file, file_type, match_data_path, player_keys_path):
    try:
        if not file.filename.lower().endswith('.csv'):
            return response("error", "The uploaded file must be a .csv file")

        df = pd.read_csv(file)

        if file_type == 'match_data':
            required_data_headers = ['Match ID', 'Team 1 P1', 'Team 1 P2', 'Team 1 P3', 'Team 1 P4', 'Team 1 P5', 'Team 1 P6', 'Team 1 P7', 'Team 1 P8', 
                'Team 2 P1', 'Team 2 P2', 'Team 2 P3', 'Team 2 P4', 'Team 2 P5', 'Team 2 P6', 'Team 2 P7', 'Team 2 P8',
                'Team 1 Goals', 'Team 2 Goals', 'Team 1 Result', 'Team 2 Result']
            upload_path = match_data_path
            
        elif file_type == 'player_keys':
            required_data_headers = ['player_name', 'player_id']
            upload_path = player_keys_path
        
        df = df.loc[:, df.columns.str.strip() != '']
        if list(df.columns) != required_data_headers:
            print(df.columns)
            return response("error", f"The column headers in your CSV file do not match the expected column headers: {required_data_headers}")
        
        df.to_csv(upload_path, index=False)

        return response("success", "File successfully uploaded")

    except Exception as e:
        return response("error", f"An error occurred: {str(e)}")


def csv_file_checker(file_path):
    """Check if a CSV file exists and contains valid data."""
    file_status = {"has_data": False}

    if not os.path.exists(file_path):
        raise MissingFileError(f"CSV file not found: {file_path}")

    with open(file_path, 'r') as file:
        content = file.read().strip()
        if content:  # Ensure it's not just whitespace
            file_status["has_data"] = True
    
    return file_status

def json_file_checker(file_path):
    """Check if a JSON file exists and contains valid data."""
    file_status = {"has_data": False}

    if not os.path.exists(file_path):
        raise MissingFileError(f"JSON file not found: {file_path}")

    with open(file_path, 'r') as file:
        content = file.read().strip()
        if content:  # Ensure it's not just whitespace
            file_status["has_data"] = True

    return file_status
















# def validate_data(match_data_path, match_count_path):
#     match_data = pd.read_csv(match_data_path)
#     match_data_match_count = match_data['Match ID'].max()

#     with open(match_count_path, 'r') as file:
#          player_stats_match_count = file.read().strip()
#          if not player_stats_match_count:
#               return response("warning", "Cannot detect whether the player stats table is reflective of the match_data file")
         
#          if player_stats_match_count != int(match_data_match_count):
#               return response("warning", "Player stats table is not reflective of the match_data file")
         
#     return response("success", "Player stats matches match the number of matches in match_data file")


# def initialisation_playerstats_playerform(player_stats_path, player_keys_path, match_data_path, match_count_path, player_form_dict_path):
#     """Initialize player stats and form data."""
#     # Check if player stats file exists
#     player_stats_df = csv_file_checker(player_stats_path)
    
#     if player_stats_df is None:
#         # Player stats not found, check for match data
#         match_data_df = csv_file_checker(match_data_path)
#         if match_data_df is None:
#             # Match data missing, cannot proceed
#             return response("error", "Upload match data to visualize stats.")

#         # Create player stats and form files
#         player_stats_df, player_form_dict = create_player_stats_and_form(
#             match_data_path, match_count_path, player_keys_path, player_stats_path, player_form_dict_path
#         )
#     else:
#         # Load existing player stats and form
#         player_form_dict = json_file_checker(player_form_dict_path)
#         if not player_form_dict:
#             # If JSON is missing or invalid, create it
#             match_data_df = csv_file_checker(match_data_path)
#             if match_data_df is None:
#                 return "error", "Upload match data to visualize stats."
#             player_form_dict = raw_data_processing.create_save_player_form_dict(
#                 match_data_path, match_count_path, player_form_dict_path
#             )

#     # Return data for further use
#     return player_stats_df, player_form_dict