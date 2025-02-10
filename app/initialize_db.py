import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Colors
GREEN = "\033[92m"  # Bright Green
RED = "\033[91m"    # Bright Red
RESET = "\033[0m"   # Reset to default color

#Postgres database connection
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
)

#Initialize database and create tables
def initialize_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        #Create tables
        create_tables = '''
        CREATE TABLE IF NOT EXISTS events (
            GW_id INT PRIMARY KEY,
            name VARCHAR(50),
            finished BOOLEAN,
            average_GW_score INT,
            highest_scoring_playerid FLOAT,
            highest_GW_score FLOAT,
            most_selected_player FLOAT,
            most_transferred_in_player FLOAT,
            top_player FLOAT,
            transfers_made INT,
            most_captained FLOAT,
            most_vice_captained FLOAT,
            deadline_time DATE
        );
    
        
        CREATE TABLE IF NOT EXISTS fixtures_stats_eachplayer (
            GW_id INT,
            fixture_id INT,
            player_id INT,
            player_name VARCHAR(255),
            stat_type VARCHAR(255),
            stat_value INT,
            PRIMARY KEY(GW_id, fixture_id, player_id, stat_type)
        );
        
        CREATE TABLE IF NOT EXISTS fixtures_stats_overview (
            GW_id INT,
            fixture_id INT,
            finished BOOLEAN,
            hometeam_id INT,
            awayteam_id INT,
            total_goals_scored INT,
            goals_by_hometeam INT,
            goals_by_awayteam INT,
            assists_by_hometeam INT,
            assists_by_awayteam INT,
            owngoals_by_hometeam INT,
            owngoals_by_awayteam INT,
            penalties_saved_hometeam INT,
            penalties_saved_awayteam INT,
            penalties_missed_hometeam INT,
            penalties_missed_awayteam INT,
            yellowcards_hometeam INT,
            yellowcards_awayteam INT,
            redcards_hometeam INT,
            redcards_awayteam INT,
            saves_hometeam INT,
            saves_awayteam INT,
            PRIMARY KEY(GW_id, fixture_id)
        );
        
        CREATE TABLE IF NOT EXISTS fixtures (
            GW_id INT,
            fixture_id INT,
            finished BOOLEAN,
            kickoff_time DATE,
            minutes INT,
            started BOOLEAN,
            away_team_id INT,
            away_team_score FLOAT,
            home_team_id INT,
            home_team_score FLOAT,
            team_h_difficulty INT,
            team_a_difficulty INT,
            PRIMARY KEY(GW_id, fixture_id)
        );
        
        CREATE TABLE IF NOT EXISTS most_chips_played_eachgw (
            GW_id INT,
            chip_played VARCHAR(100),
            num_played INT,
            PRIMARY KEY(GW_id, chip_played)
        );
        
        CREATE TABLE IF NOT EXISTS players (
            player_id INT PRIMARY KEY,
            first_name VARCHAR(255),
            second_name VARCHAR(255),
            web_name VARCHAR(255),
            can_select BOOLEAN,
            selected_by_percent FLOAT,
            status VARCHAR(10),
            total_points INT,
            transfers_in INT,
            transfers_in_event INT,
            transfers_out INT,
            transfers_out_event INT,
            region FLOAT,
            img_code VARCHAR(255),
            minutes INT,
            goals_scored INT,
            assists INT,
            clean_sheets INT,
            goals_conceded INT,
            own_goals INT,
            penalties_saved INT,
            penalties_missed INT,
            yellow_cards INT,
            red_cards INT,
            saves INT,
            bonus INT,
            bps INT,
            influence FLOAT,
            creativity FLOAT,
            threat FLOAT,
            ict_index FLOAT,
            starts INT,
            expected_goals FLOAT,
            expected_assists FLOAT,
            expected_goal_involvements FLOAT,
            expected_goals_conceded FLOAT,
            influence_rank INT,
            influence_rank_type INT,
            creativity_rank INT,
            creativity_rank_type INT,
            threat_rank INT,
            threat_rank_type INT,
            ict_index_rank INT,
            ict_index_rank_type INT,
            expected_goals_per_90 FLOAT,
            saves_per_90 FLOAT,
            expected_assists_per_90 FLOAT,
            expected_goal_involvements_per_90 FLOAT,
            expected_goals_conceded_per_90 FLOAT,
            goals_conceded_per_90 FLOAT,
            now_cost_rank INT,
            now_cost_rank_type INT,
            form_rank INT,
            form_rank_type INT,
            points_per_game_rank INT,
            points_per_game_rank_type INT,
            selected_rank INT,
            selected_rank_type INT,
            starts_per_90 FLOAT,
            clean_sheets_per_90 FLOAT,
            chance_of_playing_next_round FLOAT,
            chance_of_playing_this_round FLOAT,
            player_code INT,
            cost_change_event INT,
            cost_change_event_fall INT,
            cost_change_start INT,
            cost_change_start_fall INT,
            player_type INT,
            player_points_currentgw INT,
            form FLOAT,
            news VARCHAR(255),
            now_cost INT,
            photo VARCHAR(255),
            points_per_game FLOAT,
            team INT,
            team_code INT,
            value_form FLOAT,
            value_season FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS positions (
            position_id INT PRIMARY KEY,
            position_name VARCHAR(255),
            postion_name_short VARCHAR(255),
            squad_select INT,
            squad_min_play INT,
            squad_max_play INT,
            player_count INT
        );
        
        CREATE TABLE IF NOT EXISTS teams (
            team_id INT PRIMARY KEY,
            code INT,
            name VARCHAR(255),
            short_name VARCHAR(255),
            position INT,
            strength INT,
            strength_overall_home INT,
            strength_overall_away INT,
            strength_attack_home INT,
            strength_attack_away INT,
            strength_defence_home INT,
            strength_defence_away INT
        );
        
        CREATE TABLE IF NOT EXISTS top_player_eachgw (
            GW_id INT PRIMARY KEY,
            player_id INT,
            points INT,
            web_name VARCHAR(255),
            chance_of_playing_next_round FLOAT,
            form FLOAT,
            now_cost INT,
            total_points INT,
            transfers_in_event INT,
            transfers_out_event INT,
            img_code VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS minileague (
            entry INT PRIMARY KEY,
            id INT,
            player_name VARCHAR(255),
            entry_name VARCHAR(255),
            event_total INT,
            total INT,
            rank INT,
            last_rank INT,
            rank_sort INT,
            has_played BOOLEAN,
            last_updated_data DATE,
            league_id INT,
            league_name VARCHAR(255),
            league_created DATE
        );
        '''
        
        #Execute table creation
        cur.execute(create_tables)
        conn.commit()
        
        #Close the cursor and connection
        cur.close()
        conn.close()
        
        print(f"{GREEN}Tables created successfully!!{RESET}")
    except Exception as e:
        print(f"{RED}Error initializing database: {e}{RESET}")
        
        
if __name__ == "__main__":
    initialize_db()