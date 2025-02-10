import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Colors
GREEN = "\033[92m"  # Bright Green
RED = "\033[91m"    # Bright Red
RESET = "\033[0m"   # Reset to default color

#Database connection
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Function to read any CSV file from the data directory
def read_csv(filename):
    file_path = os.path.join(DATA_DIR, filename)  # Construct full file path
    return pd.read_csv(file_path)

def csv_to_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        #Delete old events data
        delete_query = "DELETE FROM events;"
        cur.execute(delete_query)
        
        #Load events' data
        events_df = read_csv("events.csv")
        for row in events_df.itertuples():
            cur.execute('''
                        INSERT INTO events (GW_id, name, finished, average_GW_score, highest_scoring_playerid, highest_GW_score, most_selected_player,
                        most_transferred_in_player, top_player, transfers_made, most_captained, most_vice_captained, deadline_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.GW_id, row.name, row.finished, row.average_GW_score, row.highest_scoring_playerid, row.highest_GW_score, row.most_selected_player,
                              row.most_transferred_in_player, row.top_player, row.transfers_made, row.most_captained, row.most_vice_captained, row.deadline_time)
                        )
        
        print(f"{GREEN}Events table loaded successfully!{RESET}")
            
        #Delete old fixtures_stats_eachplayer data
        delete_query = "DELETE FROM fixtures_stats_eachplayer;"
        cur.execute(delete_query)
        
        #Load fixtures_stats_eachplayer data
        fixtures_each_df = read_csv("fixtures_stats_eachplayer.csv")
        for row in fixtures_each_df.itertuples():
            cur.execute('''
                        INSERT INTO fixtures_stats_eachplayer (GW_id, fixture_id, player_id, player_name, stat_type, stat_value)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        ''', (row.GW_id, row.fixture_id, row.player_id, row.player_name, row.stat_type, row.stat_value)
                        )
        
        print(f"{GREEN}fixtures_stats_eachplayer table loaded successfully!{RESET}")
        
        #Delete old fixture_stats_overview data
        delete_query = "DELETE FROM fixtures_stats_overview;"
        cur.execute(delete_query)
        
        #Load fixture_stats_overview data
        fixtures_overview_df = read_csv("fixtures_stats_overview.csv")
        for row in fixtures_overview_df.itertuples():
            cur.execute('''
                        INSERT INTO fixtures_stats_overview (GW_id, fixture_id, finished, hometeam_id, awayteam_id, total_goals_scored, goals_by_hometeam,
                        goals_by_awayteam, assists_by_hometeam, assists_by_awayteam, owngoals_by_hometeam, owngoals_by_awayteam, penalties_saved_hometeam,
                        penalties_saved_awayteam, penalties_missed_hometeam, penalties_missed_awayteam, yellowcards_hometeam, yellowcards_awayteam, redcards_hometeam,
                        redcards_awayteam, saves_hometeam, saves_awayteam)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.GW_id, row.fixture_id, row.finished, row.hometeam_id, row.awayteam_id, row.total_goals_scored, row.goals_by_hometeam,
                              row.goals_by_awayteam, row.assists_by_hometeam, row.assists_by_awayteam, row.owngoals_by_hometeam, row.owngoals_by_awayteam,
                              row.penalties_saved_hometeam, row.penalties_saved_awayteam, row.penalties_missed_hometeam, row.penalties_missed_awayteam,
                              row.yellowcards_hometeam, row.yellowcards_awayteam, row.redcards_hometeam, row.redcards_awayteam, row.saves_hometeam, row.saves_awayteam)
                        )
        
        print(f"{GREEN}fixtures_stats_overview table loaded successfully!{RESET}")

        #Delete old fixtures data
        delete_query = "DELETE FROM fixtures;"
        cur.execute(delete_query)
        
        #Load fixtures data
        fixtures_df = read_csv("fixtures.csv")
        for row in fixtures_df.itertuples():
            cur.execute('''
                        INSERT INTO fixtures (GW_id, fixture_id, finished, kickoff_time, minutes, started, away_team_id, away_team_score, home_team_id, home_team_score,
                        team_h_difficulty, team_a_difficulty)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.GW_id, row.fixture_id, row.finished, row.kickoff_time, row.minutes, row.started, row.away_team_id, row.away_team_score, row.home_team_id,
                              row.home_team_score, row.team_h_difficulty, row.team_a_difficulty)
                        )
        
        print(f"{GREEN}fixtures table loaded successfully!{RESET}")
            
        #Delete old minileague data
        delete_query = "DELETE FROM minileague;"
        cur.execute(delete_query)
        
        #Load minileague data
        minileague_df = read_csv("minileague.csv")
        for row in minileague_df.itertuples():
            cur.execute('''
                        INSERT INTO minileague (entry, id, player_name, entry_name, event_total, total, rank, last_rank, rank_sort, has_played,
                        last_updated_data, league_id, league_name, league_created)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.entry, row.id, row.player_name, row.entry_name, row.event_total, row.total, row.rank, row.last_rank,
                              row.rank_sort, row.has_played, row.last_updated_data, row.league_id, row.league_name, row.league_created)
                        )
            
        print(f"{GREEN}minileague table loaded successfully!{RESET}")
            
        #Delete old most_chips_played_eachgw data
        delete_query = "DELETE FROM most_chips_played_eachgw;"
        cur.execute(delete_query)
        
        #Load most_chips_played_eachgw data
        most_chips_df = read_csv("most_chips_played_eachgw.csv")
        for row in most_chips_df.itertuples():
            cur.execute('''
                        INSERT INTO most_chips_played_eachgw (GW_id, chip_played, num_played)
                        VALUES (%s, %s, %s);
                        ''', (row.GW_id, row.chip_played, row.num_played)
                        )
        
        print(f"{GREEN}most_chips_played_eachgw table loaded successfully!{RESET}")
            
        #Delete old players data
        delete_query = "DELETE FROM players;"
        cur.execute(delete_query)
        
        #Load players data
        players_df = read_csv("players.csv")
        for row in players_df.itertuples():
            cur.execute('''
                        INSERT INTO players (player_id, first_name, second_name, web_name, can_select, selected_by_percent, status, total_points, transfers_in,
                        transfers_in_event, transfers_out, transfers_out_event, region, img_code, minutes, goals_scored, assists, clean_sheets,
                        goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, bonus, bps, influence, creativity, threat,
                        ict_index, starts, expected_goals, expected_assists, expected_goal_involvements, expected_goals_conceded, influence_rank, influence_rank_type,
                        creativity_rank, creativity_rank_type, threat_rank, threat_rank_type, ict_index_rank, ict_index_rank_type, expected_goals_per_90, saves_per_90,
                        expected_assists_per_90, expected_goal_involvements_per_90, expected_goals_conceded_per_90, goals_conceded_per_90, now_cost_rank, now_cost_rank_type,
                        form_rank, form_rank_type, points_per_game_rank, points_per_game_rank_type, selected_rank, selected_rank_type, starts_per_90, clean_sheets_per_90,
                        chance_of_playing_next_round, chance_of_playing_this_round, player_code, cost_change_event, cost_change_event_fall, cost_change_start, cost_change_start_fall,
                        player_type, player_points_currentgw, form, news, now_cost, photo, points_per_game, team, team_code, value_form, value_season)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.player_id, row.first_name, row.second_name, row.web_name, row.can_select, row.selected_by_percent, row.status, row.total_points, row.transfers_in,
                              row.transfers_in_event, row.transfers_out, row.transfers_out_event, row.region, row.img_code, row.minutes, row.goals_scored, row.assists,
                              row.clean_sheets, row.goals_conceded, row.own_goals, row.penalties_saved, row.penalties_missed, row.yellow_cards, row.red_cards, row.saves, row.bonus, row.bps,
                              row.influence, row.creativity, row.threat, row.ict_index, row.starts, row.expected_goals, row.expected_assists, row.expected_goal_involvements, row.expected_goals_conceded,
                              row.influence_rank, row.influence_rank_type, row.creativity_rank, row.creativity_rank_type, row.threat_rank, row.threat_rank_type, row.ict_index_rank,
                              row.ict_index_rank_type, row.expected_goals_per_90, row.saves_per_90, row.expected_assists_per_90, row.expected_goal_involvements_per_90, row.expected_goals_conceded_per_90,
                              row.goals_conceded_per_90, row.now_cost_rank, row.now_cost_rank_type, row.form_rank, row.form_rank_type, row.points_per_game_rank, row.points_per_game_rank_type,
                              row.selected_rank, row.selected_rank_type, row.starts_per_90, row.clean_sheets_per_90, row.chance_of_playing_next_round, row.chance_of_playing_this_round, row.player_code,
                              row.cost_change_event, row.cost_change_event_fall, row.cost_change_start, row.cost_change_start_fall, row.player_type, row.player_points_currentgw, row.form,
                              row.news, row.now_cost, row.photo, row.points_per_game, row.team, row.team_code, row.value_form, row.value_season)
                        )
        
        print(f"{GREEN}players table loaded successfully!{RESET}")
            
        #Delete old positions data
        delete_query = "DELETE FROM positions;"
        cur.execute(delete_query)
        
        #Load positions data
        positions_df = read_csv("positions.csv")
        for row in positions_df.itertuples():
            cur.execute('''
                        INSERT INTO positions (position_id, position_name, postion_name_short, squad_select, squad_min_play, squad_max_play, player_count)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                        ''', (row.position_id, row.position_name, row.postion_name_short, row.squad_select, row.squad_min_play, row.squad_max_play, row.player_count)
                        )
        
        print(f"{GREEN}positions table loaded successfully!{RESET}")
            
        #Delete old teams data
        delete_query = "DELETE FROM teams;"
        cur.execute(delete_query)
        
        #Load teams data
        teams_df = read_csv("teams.csv")
        for row in teams_df.itertuples():
            cur.execute('''
                        INSERT INTO teams (team_id, code, name, short_name, position, strength, strength_overall_home, strength_overall_away, strength_attack_home,
                        strength_attack_away, strength_defence_home, strength_defence_away)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.team_id, row.code, row.name, row.short_name, row.position, row.strength, row.strength_overall_home, row.strength_overall_away, row.strength_attack_home,
                              row.strength_attack_away, row.strength_defence_home, row.strength_defence_away)
                        )
        
        print(f"{GREEN}teams table loaded successfully!{RESET}")
            
        #Delete old top_player_eachgw data
        delete_query = "DELETE FROM top_player_eachgw;"
        cur.execute(delete_query)
        
        #Load top_player_eachgw data
        top_player_eachgw_df = read_csv("top_player_eachgw.csv")
        for row in top_player_eachgw_df.itertuples():
            cur.execute('''
                        INSERT INTO top_player_eachgw (GW_id, player_id, points, web_name, chance_of_playing_next_round, form, now_cost, total_points, transfers_in_event,
                        transfers_out_event, img_code)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (row.GW_id, row.player_id, row.points, row.web_name, row.chance_of_playing_next_round, row.form, row.now_cost, row.total_points,
                              row.transfers_in_event, row.transfers_out_event, row.img_code)
                        )
        
        print(f"{GREEN}top_player_eachgw table loaded successfully!{RESET}")
        
        
        conn.commit()
        
        cur.close()
        conn.close()

        print(f"{GREEN}CSV data loaded successfully!{RESET}")
    except Exception as e:
        print(f"{RED}Error loading CSV data to DB: {e}{RESET}")
        
        
if __name__ == "__main__":
    csv_to_db()