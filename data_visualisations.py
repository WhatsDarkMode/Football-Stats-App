import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as pc
import random


def get_category_colors():
    category_colors = {
            "Win": "#30952F",
            "Draw": "#FC811C",
            "Loss": "#F04040"
        }
    return category_colors

def apply_standard_layout(fig):
    fig.update_layout(
        xaxis=dict(
            title_font=dict(color="white"),  # White x-axis title
            tickfont=dict(color="white"),  # White x-axis tick labels
            showline=True,  # Show x-axis line
            linecolor="white",  # White x-axis line
            gridcolor="#444"  # Light gray gridlines
        ),
        yaxis=dict(
            title_font=dict(color="white"),  # White y-axis title
            tickfont=dict(color="white"),  # White y-axis tick labels
            showline=True,  # Show y-axis line
            linecolor="white",  # White y-axis line
            gridcolor="#444"  # Light gray gridlines
        ),
        font=dict(color="white"),  # Set all text to white
        plot_bgcolor="#2d2d2d",  # Match the dark gray background of your app
        paper_bgcolor="#2d2d2d",  # Match the dark gray background of your app
        legend=dict(font=dict(color="white")),
        hoverlabel=dict(
            font=dict(color="black"),  # Black hover text for contrast
            bgcolor="white"  # White hover background
        )
    )

def form_heatmap(player_ids, form_window, player_form_dict, player_keys_dict):
    player_match_history = {}
    max_games_played = 0
    category_colors = get_category_colors()

    for player_id in player_ids:
        match_ids = sorted(player_form_dict[player_id].keys(), key = lambda x: int(x))[-form_window:]
        player_match_history[player_id] = match_ids
        max_games_played = max(max_games_played, len(match_ids))

    form_matrix, form_text_matrix, player_names = [], [], []

    for player_id in player_ids:
        player_name = player_keys_dict[int(player_id)]
        player_names.append(player_name)

        results = []
        text_labels = []

        match_ids = player_match_history[player_id]

        for i in range(max_games_played):
            if i < len(match_ids):
                match_id = match_ids[i]
                print(match_id)
                result = float(player_form_dict[player_id][match_id])

                result_text = "Win" if result == 1 else "Draw" if result == 0.5 else "Loss"
                results.append(result)
                text_labels.append(f"{result_text} ({match_id})")
            else:
                results.append(None)
                text_labels.append("")

        form_matrix.append(results)
        form_text_matrix.append(text_labels)

    fig = go.Figure(data=go.Heatmap(
        z=form_matrix,
        x=[f"Match {i+1}" for i in range(max_games_played)],  # Arbitrary x-axis
        y=player_names,
        colorscale=[(0, category_colors["Loss"]), (0.5, category_colors["Draw"]), (1, category_colors["Win"])], 
        showscale=False,
        hoverongaps=False,
        xgap=2,
        ygap=2,
        text=form_text_matrix,  # Show result & match ID as text
        texttemplate="%{text}",
        hovertemplate="%{text}<extra></extra>"  # Ensure text is displayed
    ))
        
    for category, color in category_colors.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=10, color=color),
            name=category
        ))

    fig.update_layout(
        title=f"Player Form Over Last {form_window} Matches",
        xaxis=dict(title="Recent Matches (Oldest -> Recent)", tickangle=45),
        yaxis=dict(title="Players")
    )

    apply_standard_layout(fig)

    return pio.to_json(fig)


def goal_diff_scatter_plot(player_stats_df):
    fig = go.Figure()

    for index, player in player_stats_df.iterrows():
        player_name = player["player_name"]
        goals_for = player["total_goals_for"]
        goals_against = player["total_goals_against"]

        fig.add_trace(go.Scatter(
            x=[goals_against],
            y=[goals_for],
            mode='markers+text',
            marker=dict(size=10),#, color=dot_color),
            text=[player_name],
            name=player_name,
            textfont=dict(color="#D3D3D3"),
            showlegend=False
        ))

    # Calculate the range based on the data
    min_goals = min(player_stats_df['total_goals_for'].min(), player_stats_df['total_goals_against'].min())
    max_goals = max(player_stats_df['total_goals_for'].max(), player_stats_df['total_goals_against'].max())

    fig.add_trace(go.Scatter(
        x=[0, max_goals],  # Dummy x values (will be scaled by Plotly)
        y=[0, max_goals],  # Dummy y values (will be scaled by Plotly)
        mode='lines',
        name='x=y',
        line=dict(color='#9370DB', width=2),
        showlegend=False
    ))

    fig.update_layout(
        title="Goals For vs Goals Against",
        xaxis_title="Goals Against",
        yaxis_title="Goals For",
        xaxis=dict(range=[min_goals, max_goals + 5]),  # Set x-axis range
        yaxis=dict(range=[min_goals, max_goals + 5])  # Set y-axis range
    )

    apply_standard_layout(fig)

    return pio.to_json(fig)


def results_bar_graph(player_stats_df):
    # Extract player names and stats
    player_names = player_stats_df["player_name"].tolist()
    wins = player_stats_df["total_wins"].tolist()
    draws = player_stats_df["total_draws"].tolist()
    losses = player_stats_df["total_losses"].tolist()

    category_colors = get_category_colors()

    # Create a single bar trace per category
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=player_names, y=wins, name='Wins', marker_color=category_colors["Win"]))
    fig.add_trace(go.Bar(x=player_names, y=draws, name='Draws', marker_color=category_colors["Draw"]))
    fig.add_trace(go.Bar(x=player_names, y=losses, name='Losses', marker_color=category_colors["Loss"]))

    # Update layout for stacked bar chart
    fig.update_layout(
        title="Wins, Draws, and Losses (Stacked Bar Chart)",
        xaxis_title="Players",
        yaxis_title="Number of Matches",
        barmode='stack'  # Stack bars on top of each other
    )

    apply_standard_layout(fig)

    return pio.to_json(fig)