import pandas as pd
import base64
import io

def validate_data(match_data_path, match_count_path):
    """
    Checks whether the calculated stats is based on the current raw data csv
    """
    raw_data = pd.read_csv(match_data_path)
    match_count_from_raw_data = raw_data['Match ID'].max()

    try:
        with open(match_count_path, 'r') as file:
            stored_match_count = int(file.read().strip())
    except FileNotFoundError:
        return {
            "valid": False,
            "message": f"Match count file '{match_count_path}' not found"
        }
    
    if match_count_from_raw_data != stored_match_count:
        return {
            "valid": False,
            "message": f"Discrepancy detected: Raw data has {match_count_from_raw_data} matches, "
                       f"but calculated stats are based on {stored_match_count} matches."
        }
    
    return {"valid": True, "message": "Data is valid"}

def app_initialisation_validate_data_check(data_trigger, match_data_path, match_count_path):
    """
    This function validates the data when the app is initialised.
    This function should be connected to a callback in the app.py file.
    The callback needs 3 inputs: app-load-trigger data, raw-data-path, and match-count.
    """
    if data_trigger.get('loaded', False):
        result = validate_data(match_data_path, match_count_path)
        if not result['valid']:
            return True, result['message'], "danger"
        
        return False, "", "success"
    
    return False, "", "success"

def handle_match_data_upload(filename, contents):
    """
    Handles the uploaded match_data file, validates its structure and saves it.
    The call back needs to provide 2 inputs: filename and contents.
    """
    if not filename.lower().endwith('.csv'):
        return {
            "status": "error",
            "message": "The uploaded file must be a csv"
        }

    try:
        # Decode the Base64 contents
        content_type, content_string = contents.split(',')
        decoded_bytes = base64.b64decode(content_string)
        decoded_text = decoded_bytes.decode('utf-8')

        # Parse decoded contents into a DataFrame
        df = pd.read_csv(io.StringIO(decoded_text))

        required_data_headers = ['Match ID', 'Team 1 P1', 'Team 1 P2', 'Team 1 P3', 'Team 1 P4', 'Team 1 P5', 'Team 1 P6', 'Team 1 P7', 'Team 1 P8', 
                                 'Team 2 P1', 'Team 2 P2', 'Team 2 P3', 'Team 2 P4', 'Team 2 P5', 'Team 2 P6', 'Team 2 P7', 'Team 2 P8',
                                  'Team 1 Goals', 'Team 2 Goals', 'Team 1 Result', 'Team 2 Result']
        if set(df.columns) != set(required_data_headers):
            return {
                "status": "error",
                "message": "The uploaded file does not contain the correct data headers."
            }

        save_path = r'C:\My Documents\football\data\raw\match_data.csv'
        df.to_csv(save_path, index=False)

        return {
            "status": "complete",
            "message": "Match data file uploaded and saved successfully"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"An error occurred: {str(e)}"
            }

def handle_player_keys_upload(filename, contents):
    """
    Handles the uploaded player_keys file, validates its structure and saves it.
    The call back needs to provide 2 inputs: filename and contents.
    """
    if not filename.lower().endwith('.csv'):
        return {
            "status": "error",
            "message": "The uploaded file must be a csv"
        }

    try:
        # Decode the Base64 contents
        content_type, content_string = contents.split(',')
        decoded_bytes = base64.b64decode(content_string)
        decoded_text = decoded_bytes.decode('utf-8')

        # Parse decoded contents into a DataFrame
        df = pd.read_csv(io.StringIO(decoded_text))

        required_data_headers = ['player name', 'player_ID']
        if set(df.columns) != set(required_data_headers):
            return {
                "status": "error",
                "message": "The uploaded file does not contain the correct data headers."
            }

        save_path = r'C:\My Documents\football\data\raw\player_keys.csv'
        df.to_csv(save_path, index=False)

        return {
            "status": "complete",
            "message": "Match data file uploaded and saved successfully"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"An error occurred: {str(e)}"
            }