
from collections import deque
from ..environment.game import PacmanGame
import time
from copy import deepcopy

def bfs_solver(game: PacmanGame, timeout=200):
    start_time = time.time()

    initial_game_state = game.get_state()
    initial_snacks = deepcopy(game.snacks)
    num_ghosts = len(game.ghosts)
    
    queue = deque([(game, [])])
    visited = {initial_game_state}
    found_path = None

    while queue:
        if time.time() - start_time > timeout:
            print("BFS solver timed out during search.")
            return None

        current_game, path_to_current = queue.popleft()

        if current_game.is_goal():
            found_path = path_to_current
            print(f"BFS found a solution with path length: {len(found_path)}")
            break

        for next_game_instance, action, _ in current_game.get_next_states():
            next_state_tuple = next_game_instance.get_state()
            if next_state_tuple not in visited:
                visited.add(next_state_tuple)
                new_path = path_to_current + [action]
                queue.append((next_game_instance, new_path))

    if found_path is None:
        print("BFS search completed. No solution found.")
        return None

    raw_history = []
    sim_game = deepcopy(game)
    _, initial_info_list = sim_game.get_info()
    raw_history.append(('', initial_info_list))

    for move in found_path:
        for next_game, action, _ in sim_game.get_next_states():
            if action == move:
                sim_game = next_game
                _, next_info_list = sim_game.get_info()
                raw_history.append((move, next_info_list))
                break
    final_render_history = []
    for move, raw_info in raw_history:
        player_info = raw_info[0]
        ghosts_info = raw_info[1 : 1 + num_ghosts]
        current_snacks_tuples = raw_info[1 + num_ghosts:]
        

        current_snack_map = {}
        for s_row, s_col, s_type, s_exists in current_snacks_tuples:
            current_snack_map[(s_row, s_col)] = (s_type, s_exists)

        formatted_snack_info = []
        for s in initial_snacks:
            snack_status = current_snack_map.get((s.x, s.y)) 
            if snack_status:
                s_type, s_exists = snack_status
                formatted_snack_info.append((s.x, s.y, s_type, s_exists))
            else:
                formatted_snack_info.append((s.x, s.y, s.type, False))
                        
        final_info_list = [player_info] + ghosts_info + formatted_snack_info
        final_render_history.append((move, final_info_list))

    return final_render_history
