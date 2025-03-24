import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# File paths
MATCH_DATA_PATH = os.path.join(BASE_DIR, 'data/raw/match_data.csv')
PLAYER_KEYS_PATH = os.path.join(BASE_DIR, 'data/raw/player_keys.csv')
MATCH_COUNT_PATH = os.path.join(BASE_DIR, 'data/calculated/match_count.txt')
PLAYER_STATS_PATH = os.path.join(BASE_DIR, 'data/calculated/player_stats.csv')
PLAYER_FORM_DICT_PATH = os.path.join(BASE_DIR, 'data/calculated/player_form_dict.json')

# SSL Context
SSL_CONTEXT = (os.path.join(BASE_DIR, 'ssl/client-cert.pem'),
               os.path.join(BASE_DIR, 'ssl/client-key.pem'))
