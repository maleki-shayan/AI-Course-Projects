# File: core/solvers/ids_solver.py

from ..environment.game import PacmanGame
from copy import deepcopy
import time

def dls_solver(game: PacmanGame, depth_limit: int, path: list, visited: set):
    """
    Depth-Limited Search (DLS) helper function for IDS.
    """
    if game.is_goal():
        return path

    if depth_limit == 0:
        return None

    current_state = game.get_state()
    visited.add(current_state)

    for next_game, action, _ in game.get_next_states():
        next_state = next_game.get_state()
        if next_state not in visited:
            new_path = path + [action]
            result = dls_solver(next_game, depth_limit - 1, new_path, visited.copy())
            if result is not None:
                return result

    return None

def ids_solver(game: PacmanGame, timeout=60):

    start_time = time.time()
    
    initial_game_state = deepcopy(game)
    initial_snacks = initial_game_state.snacks
    num_ghosts = len(initial_game_state.ghosts)
    
    found_path = None
    
    print("IDS: Starting search...")
    for depth in range(1, 1000):  
        if time.time() - start_time > timeout:
            print("IDS solver timed out.")
            return None
        
        print(f"IDS: Trying depth {depth}...")
        
        visited_in_path = {game.get_state()}
        result_path = dls_solver(deepcopy(game), depth, [], visited_in_path)
        
        if result_path is not None:
            print(f"IDS: Found a solution at depth {depth} with {len(result_path)} moves.")
            found_path = result_path
            break
            
    if found_path is None:
        print("IDS search completed. No solution found.")
        return None

    raw_history = []
    sim_game = deepcopy(initial_game_state)
    _, initial_info_list = sim_game.get_info()
    raw_history.append(('', initial_info_list))

    for move in found_path:
        action_found = False
        for next_game_state, action, _ in sim_game.get_next_states():
            if action == move:
                sim_game = next_game_state
                _, next_info_list = sim_game.get_info()
                raw_history.append((move, next_info_list))
                action_found = True
                break
        if not action_found:
            print(f"Error: Could not simulate move '{move}' during history generation.")
            return None # 

    final_render_history = []
    for move, raw_info in raw_history:
        player_info = raw_info[0]
        ghosts_info = raw_info[1 : 1 + num_ghosts]
        current_snacks_tuples = raw_info[1 + num_ghosts:]
        
        current_snack_map = { (s_row, s_col): (s_type, s_exists) for s_row, s_col, s_type, s_exists in current_snacks_tuples }

        formatted_snack_info = []
        for s in initial_snacks:
            snack_pos_key = (s.y, s.x)
            if snack_pos_key in current_snack_map:
                s_type, s_exists = current_snack_map[snack_pos_key]
                formatted_snack_info.append((s.y, s.x, s_type, s_exists))
            else: 
                formatted_snack_info.append((s.y, s.x, s.type, False))
        
        final_info_list = [player_info] + ghosts_info + formatted_snack_info
        final_render_history.append((move, final_info_list))

    print(f"IDS history generated successfully with {len(final_render_history)} states.")
    return final_render_history
