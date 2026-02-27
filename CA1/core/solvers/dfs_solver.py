# File: core/solvers/dfs_solver.py

from ..environment.game import PacmanGame
from copy import deepcopy
import time

def dfs_solver(game: PacmanGame, timeout=120):

    start_time = time.time()

    initial_game = deepcopy(game)
    initial_state = initial_game.get_state()
    initial_snacks = deepcopy(initial_game.snacks)
    num_ghosts = len(initial_game.ghosts)

    stack = [(deepcopy(game), [])] 
    visited = {initial_state}
    found_path = None

    print("DFS: Starting search...")

    while stack:
        if time.time() - start_time > timeout:
            print("DFS: Timeout reached.")
            return None

        current_game, path = stack.pop()

        if current_game.is_goal():
            found_path = path
            print(f"DFS: Goal found! Path length = {len(found_path)}")
            break

        next_states = current_game.get_next_states()
        for next_game, action, _ in reversed(next_states):
            state = next_game.get_state()
            if state not in visited:
                visited.add(state)
                stack.append((next_game, path + [action]))

    if found_path is None:
        print("DFS: No solution found.")
        return None


    sim_game = deepcopy(initial_game)
    raw_history = []

    _, first_info = sim_game.get_info()
    raw_history.append(('', first_info))

    for move in found_path:
        for next_game, action, _ in sim_game.get_next_states():
            if action == move:
                sim_game = next_game
                _, frame_info = sim_game.get_info()
                raw_history.append((action, frame_info))
                break

    print("DFS: Building GUI-safe render history...")
    final_render_history = []

    for move, raw_info in raw_history:
        player_info = raw_info[0]
        ghosts_info = raw_info[1 : 1 + num_ghosts]
        current_snacks = raw_info[1 + num_ghosts :]

        snack_map = {(sx, sy): (stype, sexists)
                     for sx, sy, stype, sexists in current_snacks}

        ordered_snacks = []
        for s in initial_snacks:
            pos = (s.x, s.y)
            if pos in snack_map:
                stype, sexists = snack_map[pos]
                ordered_snacks.append((s.x, s.y, stype, sexists))
            else:
                ordered_snacks.append((s.x, s.y, s.type, False))

        final_info = [player_info] + ghosts_info + ordered_snacks
        final_render_history.append((move, final_info))

    print(f"DFS: History ready ({len(final_render_history)} frames).")
    return final_render_history
