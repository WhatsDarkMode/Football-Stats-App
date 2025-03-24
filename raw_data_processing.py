import pandas as pd
import json
from collections import defaultdict
from display import response


def process_match_data(match_data_path, match_count_path):
    player_records = []
    player_form_dict = defaultdict(lambda:{})
    match_data = pd.read_csv(match_data_path)

    for index, row in match_data.iterrows():
        players_team1 = [row[f'Team 1 P{i}'] for i in range(1,9) if row[f'Team 1 P{i}'] != 0] # gets list of players in team 1 for that match
        players_team2 = [row[f'Team 2 P{i}'] for i in range(1,9) if row[f'Team 2 P{i}'] != 0] # gets list of players in team 2 for that match

        for team, players in [('Team 1', players_team1), ('Team 2', players_team2)]:
            for player_id in players:
                player_records.append({
                    'match_id': int(row['Match ID']),
                    'player_id': int(player_id),
                    'team': team,
                    'goals_for': int(row[f'{team} Goals']),
                    'goals_against': int(row['Team 2 Goals'] if team == 'Team 1' else row['Team 1 Goals']),
                    'result': str(row[f'{team} Result']).strip()
                })

                player_form_dict[int(player_id)][int(row['Match ID'])] = str(row[f'{team} Result']).strip()

    total_number_of_matches = match_data['Match ID'].max()
    with open(match_count_path, 'w') as file:
        file.write(str(total_number_of_matches))

    return player_records, player_form_dict
    

def calculate_player_stats(player_records):
    calculated_player_stats = {}

    for player_record in player_records:
        player_id = player_record['player_id']

        if player_id not in calculated_player_stats:
            calculated_player_stats[player_id] = {
                'total_matches': 0,
                'total_wins': 0,
                'total_draws': 0,
                'total_losses': 0,
                'total_goals_for': 0,
                'total_goals_against': 0,
                'win_pct': 0,
                'draw_pct': 0,
                'loss_pct': 0
            }

        calculated_player_stats[player_id]['total_matches'] += 1
        calculated_player_stats[player_id]['total_goals_for'] += player_record['goals_for']
        calculated_player_stats[player_id]['total_goals_against'] += player_record['goals_against']

        if player_record['result'] == "1.0":
            calculated_player_stats[player_id]['total_wins'] += 1
        elif player_record['result'] == "0.5":
            calculated_player_stats[player_id]['total_draws'] += 1
        else:
            calculated_player_stats[player_id]['total_losses'] += 1

    for player_id, stats in calculated_player_stats.items():
        total_matches = stats['total_matches']
        if total_matches > 0:
            stats['win_pct'] = round(stats['total_wins'] / total_matches * 100, 1)
            stats['draw_pct'] = round(stats['total_draws'] / total_matches * 100, 1)
            stats['loss_pct'] = round(stats['total_losses'] / total_matches * 100, 1)
    
    return calculated_player_stats


def cs_player_stats_player_form(match_data_path, match_count_path, player_keys_path, player_stats_path, player_form_dict_path):
    player_records, player_form_dict = process_match_data(match_data_path, match_count_path)
    calculated_player_stats = calculate_player_stats(player_records)

    player_keys = pd.read_csv(player_keys_path)
    player_stats_df = pd.DataFrame.from_dict(calculated_player_stats, orient='index')
    player_stats_df = player_stats_df.reset_index().rename(columns={'index': 'player_id'})
    player_stats_df = player_stats_df.merge(player_keys, how='left', left_on='player_id', right_on='player_id')
    player_stats_df = player_stats_df.drop(columns=['player_id']) 

    player_stats_df = player_stats_df.set_index('player_name').reset_index()

    player_stats_df.to_csv(player_stats_path, index=False) # saves the df

    with open(player_form_dict_path, 'w') as file: # saves player_form_dict
        json.dump(player_form_dict, file)

    return player_stats_df, player_form_dict

