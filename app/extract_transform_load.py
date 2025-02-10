import os
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
API_BASE_URL = 'https://fantasy.premierleague.com/api/'

# Colors
GREEN = "\033[92m"  # Bright Green
RED = "\033[91m"    # Bright Red
RESET = "\033[0m"   # Reset to default color

# Function to read any CSV file from the data directory
def read_csv(filename):
    file_path = os.path.join(DATA_DIR, filename)  # Construct full file path
    return pd.read_csv(file_path)

#Transform players' data
def transform_players(data):
    df = pd.DataFrame(data)
    df = df.drop(columns=['can_transact', 'dreamteam_count', 'ep_next', 'ep_this', 'in_dreamteam', 'removed', 'special', 
                          'squad_number', 'has_temporary_code', 'mng_win', 'mng_draw', 'mng_loss', 'mng_underdog_win', 'mng_underdog_draw',
                          'mng_clean_sheets', 'mng_goals_scored', 'corners_and_indirect_freekicks_order', 'corners_and_indirect_freekicks_text',
                          'direct_freekicks_order', 'direct_freekicks_text', 'penalties_order', 'penalties_text'], errors='ignore')
    df = df.rename(columns={'code':'player_code', 'element_type': 'player_type', 'event_points':'player_points_currentgw', 'id':'player_id',
                            'opta_code':'img_code'})
    
    return df

#Transform Teams' data
def transform_teams(data):
    df = pd.DataFrame(data)
    df = df.drop(columns=['draw', 'form', 'loss', 'played', 'points', 'team_division', 'unavailable', 'win', 'pulse_id'], errors='ignore')
    df = df.rename(columns={'id':'team_id'})
    return df

#Transfrom Gameweek data
def transform_events(data):
    df = pd.DataFrame(data)
    
    #Drop irrelevant columns
    df = df.drop(columns=['release_time', 'data_checked', 'deadline_time_epoch', 'deadline_time_game_offset',
                          'is_previous', 'is_current', 'is_next', 'cup_leagues_created', 'h2h_ko_matches_created', 'can_enter',
                          'can_manage', 'released', 'ranked_count', 'overrides'], errors='ignore')
    
    #Rename column names for clarity
    df = df.rename(columns={'id':'GW_id', 'average_entry_score': 'average_GW_score', 'highest_scoring_entry': 'highest_scoring_playerid',
                            'highest_score': 'highest_GW_score', 'most_selected': 'most_selected_player', 'most_transferred_in': 'most_transferred_in_player',
                            'top_element': 'top_player', 'top_element_info':'top_player_info'})
    
    #Calculate the most number of chips played each GW and save to a new file
    if 'chip_plays' in df.columns:
        chips_list = []
        
        for _, row in df.iterrows():
            gw_id = row['GW_id']
            if isinstance(row['chip_plays'], list):
                for chip in row['chip_plays']:
                    chips_list.append({
                        'GW_id': gw_id,
                        'chip_played': chip['chip_name'],
                        'num_played': chip['num_played']
                    })
        
        chips_df = pd.DataFrame(chips_list)
        save_data_to_csv(chips_df, 'most_chips_played_eachgw.csv')
        df = df.drop(columns=['chip_plays'], errors='ignore')
    
    #Calculate the most points scored player each gw and save to a new file
    if 'top_player_info' in df.columns:
        top_players_list = []
        
        for _, row in df.iterrows():
            gw_id = row['GW_id']
            if isinstance(row['top_player_info'], dict):
                top_players_list.append({
                    'GW_id': gw_id,
                    'player_id': row['top_player_info']['id'],
                    'points': row['top_player_info']['points']
                })
                
        # Convert to DataFrame
        top_players_df = pd.DataFrame(top_players_list)
        
        # Load players.csv to join player details
        players_df = read_csv('players.csv')
        
        players_df = players_df[['player_id', 'web_name', 'chance_of_playing_next_round', 'form', 'now_cost', 'total_points',
                                 'transfers_in_event', 'transfers_out_event', 'img_code']]
        
        merged_df = top_players_df.merge(players_df, on='player_id', how='left')
        
        save_data_to_csv(merged_df, 'top_player_eachgw.csv')
        df = df.drop(columns=['top_player_info'], errors='ignore')

        
    return df

#Transform positions' data
def transform_positions(data):
    df = pd.DataFrame(data)
    df = df.drop(columns=['singular_name' , 'singular_name_short', 'squad_min_select', 'squad_max_select', 'ui_shirt_specific', 'sub_positions_locked'], errors='ignore')
    df = df.rename(columns={'id':'position_id', 'plural_name': 'position_name', 'plural_name_short': 'postion_name_short', 'element_count': 'player_count'})
    
    return df

#Transform fixtures' data
def transform_fixtures(data):
    df = pd.DataFrame(data)
    
    df = df.drop(columns=['finished_provisional', 'code', 'provisional_start_time', 'pulse_id'], errors='ignore')
    df = df.rename(columns={'event':'GW_id', 'id':'fixture_id', 'team_a':'away_team_id', 'team_a_score':'away_team_score', 
                            'team_h':'home_team_id', 'team_h_score':'home_team_score'})
    
    #Remove rows where 'GW_id' is empty
    df = df[df['GW_id'].notna()]
    
    # Stats table
    fixtures_stats_overview = []
    
    for _, row in df.iterrows():
        if pd.isnull(row['GW_id']):
            continue
        gw_id = row['GW_id']
        fixture_id = row['fixture_id']
        awayteam_id = row['away_team_id']
        hometeam_id = row['home_team_id']
        finished = row['finished']
        overview_stats_dict = {
            'GW_id': gw_id,
            'fixture_id': fixture_id,
            'finished': finished,
            'hometeam_id': hometeam_id,
            'awayteam_id': awayteam_id,
            'total_goals_scored': 0,
            'goals_by_hometeam': 0,
            'goals_by_awayteam': 0,
            'assists_by_hometeam': 0,
            'assists_by_awayteam': 0,
            'owngoals_by_hometeam': 0,
            'owngoals_by_awayteam': 0,
            'penalties_saved_hometeam': 0,
            'penalties_saved_awayteam': 0,
            'penalties_missed_hometeam': 0,
            'penalties_missed_awayteam': 0,
            'yellowcards_hometeam': 0,
            'yellowcards_awayteam': 0,
            'redcards_hometeam': 0,
            'redcards_awayteam': 0,
            'saves_hometeam': 0,
            'saves_awayteam': 0   
        }
        
        for stat in row.get('stats', []):
            identifier = stat['identifier']
            home_events = stat['h']
            away_events = stat['a']
            
            # Sum up values for each stat type
            if identifier == 'goals_scored':
                overview_stats_dict['goals_by_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['goals_by_awayteam'] = sum(item['value'] for item in away_events)
                overview_stats_dict['total_goals_scored'] = overview_stats_dict['goals_by_hometeam'] + overview_stats_dict['goals_by_awayteam']
            elif identifier == 'assists':
                overview_stats_dict['assists_by_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['assists_by_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'own_goals':
                overview_stats_dict['owngoals_by_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['owngoals_by_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'penalties_saved':
                overview_stats_dict['penalties_saved_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['penalties_saved_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'penalties_missed':
                overview_stats_dict['penalties_missed_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['penalties_missed_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'yellow_cards':
                overview_stats_dict['yellowcards_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['yellowcards_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'red_cards':
                overview_stats_dict['redcards_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['redcards_awayteam'] = sum(item['value'] for item in away_events)
            elif identifier == 'saves':
                overview_stats_dict['saves_hometeam'] = sum(item['value'] for item in home_events)
                overview_stats_dict['saves_awayteam'] = sum(item['value'] for item in away_events)
        
        fixtures_stats_overview.append(overview_stats_dict)
        
    fixtures_overview_df = pd.DataFrame(fixtures_stats_overview)
    save_data_to_csv(fixtures_overview_df, 'fixtures_stats_overview.csv')
        
    # Individual stats for each fixture
    df_players = read_csv('players.csv')
    fixtures_stats_eachplayer = []
    
    for _, row in df.iterrows():
        # Skip fixtures that are not finished
        if not row['finished']:
            continue
        gw_id = row['GW_id']
        fixture_id = row['fixture_id']
        # finished = row['finished']
        bps_players = []
        
        for stat in row.get('stats', []):
            stat_type = stat['identifier']
            home_events = stat['h']
            away_events = stat['a']
            
            for event in home_events + away_events:
                player_id = event['element']
                stat_value = event['value']
                
                #Fetch player name from players.csv
                player_info = df_players[df_players['player_id'] == player_id]
                player_name = player_info['web_name'].values[0] if not player_info.empty else 'Unknown'
                
                stat_mappings = {
                    'goals_scored': 'goal',
                    'assists': 'assist',
                    'penalties_saved': 'penalty_saved',
                    'penalties_missed': 'penalty_missed',
                    'yellow_cards': 'yellow_card',
                    'red_cards': 'red_card',
                    'saves': 'save',
                    'bonus': 'bonus',
                    'bps': 'bps'
                }
                
                stat_type_clean = stat_mappings.get(stat_type, stat_type)
                
                if stat_type_clean == "bps":
                    # Collect BPS players to filter top 4 later
                    bps_players.append({
                        'GW_id': gw_id,
                        'fixture_id': fixture_id,
                        'player_id': player_id,
                        'player_name': player_name,
                        'stat_type': stat_type_clean,
                        'stat_value': stat_value
                    })
                else:
                    # Add other stats directly
                    fixtures_stats_eachplayer.append({
                        'GW_id': gw_id,
                        'fixture_id': fixture_id,
                        'player_id': player_id,
                        'player_name': player_name,
                        'stat_type': stat_type_clean,
                        'stat_value': stat_value
                    })
                    
        # Keep only the top 4 BPS players for each fixture
        if bps_players:
            top_bps_players = sorted(bps_players, key=lambda x: x['stat_value'], reverse=True)[:4]
            fixtures_stats_eachplayer.extend(top_bps_players)
                
    fixtures_eachplayer_df = pd.DataFrame(fixtures_stats_eachplayer)
    save_data_to_csv(fixtures_eachplayer_df, 'fixtures_stats_eachplayer.csv')
    df = df.drop(columns=['stats'], errors='ignore')    
                    
    return df

#Transform minileague data(personal minileague)
def transform_minileague(data):
    last_updated_data = data.get('last_updated_data')
    league_data = data.get('league', {})
    
    league_id = league_data.get('id')
    league_name = league_data.get('name')
    league_created = league_data.get('created')
    
    standings = data.get('standings', {}).get('results', [])
    df = pd.DataFrame(standings) if standings else pd.DataFrame(columns=['entry', 'player_name'])

    
    df['last_updated_data'] = last_updated_data
    df['league_id'] = league_id
    df['league_name'] = league_name
    df['league_created'] = league_created
    
    return df

ENDPOINTS_BOOTSTRAP = {
    'elements': {
        'filename': 'players.csv',
        'transform_func': transform_players
    },
    'teams': {
        'filename': 'teams.csv',
        'transform_func': transform_teams
    },
    'events': {
        'filename': 'events.csv',
        'transform_func': transform_events
    },
    'element_types': {
        'filename': 'positions.csv',
        'transform_func': transform_positions
    },
}

ENDPOINTS_FIXTURES = {
    'fixtures': {
        'url': 'https://fantasy.premierleague.com/api/fixtures/',
        'filename': 'fixtures.csv',
        'transform_func': transform_fixtures
    }
}

ENDPOINTS_MINILEAGUE = {
    'standings': {
        'url': API_BASE_URL + 'leagues-classic/655538/standings/', #change the minileague ID for your own minileague data
        'filename': 'minileague.csv',
        'transform_func': transform_minileague
    }
}

#Save transformed data to csv
def save_data_to_csv(data, filename):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, filename)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    data.to_csv(filepath, index=False)


#Extract key information from the bootstrap API
def extract_bootstrap_data():
    bootstrap_url = API_BASE_URL + 'bootstrap-static/'
    try:
        response = requests.get(bootstrap_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return
    data = response.json()

    for key, config in ENDPOINTS_BOOTSTRAP.items():
        raw_data = data.get(key)
        # print('raw_data: ', raw_data)
        if raw_data is None:
            print(f"Warning: No data found for key: {key}")
            continue
        transform_func = config.get('transform_func')
        # print('transform_func', transform_func)
        df = transform_func(raw_data)
        # print('df', df)
        filename = config.get('filename')
        # print('filename', filename)
        save_data_to_csv(df, filename)
        print(f"{GREEN}Cleaned bootstrap data successfully!{RESET}")

#Extract fixtures' information from the fixtures API
def extract_fixtures_data():
    fixtures_config = ENDPOINTS_FIXTURES['fixtures']
    fixtures_url = fixtures_config.get('url')
    try:
        response = requests.get(fixtures_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return
    data = response.json()

    transform_func = fixtures_config.get('transform_func')
    df = transform_func(data)
    filename = fixtures_config.get('filename')
    save_data_to_csv(df, filename)
    print(f"{GREEN}Cleaned fixtures data successfully!{RESET}")

#Extract minileague data    
def extract_minileague_data():
    minileague_config = ENDPOINTS_MINILEAGUE['standings']
    minileague_url = minileague_config.get('url')
    response = requests.get(minileague_url)
    data = response.json()
    
    transform_func = minileague_config.get('transform_func')
    df = transform_func(data)
    filename = minileague_config.get('filename')
    save_data_to_csv(df, filename)
    print(f"{GREEN}Cleaned minileague data successfully!{RESET}")

def extract_data():
    extract_bootstrap_data()
    extract_fixtures_data()
    extract_minileague_data()

if __name__ == "__main__":
    extract_data()