# File: core/solvers/weighted_astar_solver.py

from ..environment.game import PacmanGame
from .heuristics import farthest_snack_heuristic
from copy import deepcopy
import time


def weighted_astar_solver(game: PacmanGame, heuristic_func=farthest_snack_heuristic, weight: int = 5, timeout: int = 120):

    start_time = time.time()

    initial_game = deepcopy(game)
    initial_state = initial_game.get_state()
    initial_snacks = deepcopy(initial_game.snacks)
    num_ghosts = len(initial_game.ghosts)

    g_costs = {initial_state: 0}
    h_init = heuristic_func(initial_game)
    f_init = g_costs[initial_state] + weight * h_init

    open_list = [(f_init, g_costs[initial_state], initial_game, [])]
    visited = set()

    found_path = None

    while open_list:
        if time.time() - start_time > timeout:
            print("Weighted A*: Timeout reached.")
            return None

        best_index = 0
        for i in range(1, len(open_list)):
            if open_list[i][0] < open_list[best_index][0]:
                best_index = i

        f_cost, g_cost, current_game, path = open_list.pop(best_index)
        current_state = current_game.get_state()

        if current_state in visited:
            continue
        visited.add(current_state)

        if current_game.is_goal():
            found_path = path
            print(f"Weighted A*: Goal reached. Path length = {len(found_path)}")
            break

        for next_game, action, cost in current_game.get_next_states():
            next_state = next_game.get_state()
            new_g = g_cost + cost
            new_h = heuristic_func(next_game)
            new_f = new_g + weight * new_h

            if next_state not in g_costs or new_g < g_costs[next_state]:
                g_costs[next_state] = new_g
                open_list.append((new_f, new_g, next_game, path + [action]))

    if found_path is None:
        print("Weighted A*: No solution found.")
        return None

    print("Weighted A*: Replaying path for renderer...")
    sim_game = deepcopy(initial_game)
    raw_history = []

    _, info0 = sim_game.get_info()
    raw_history.append(('', info0))

    for move in found_path:
        for next_game, action, _ in sim_game.get_next_states():
            if action == move:
                sim_game = next_game
                _, info_next = sim_game.get_info()
                raw_history.append((action, info_next))
                break

    print("Weighted A*: Building GUI-safe render history...")
    gui_history = []
    for move, raw_info in raw_history:
        player_info = raw_info[0]
        ghosts_info = raw_info[1:1+num_ghosts]
        current_snacks_tuples = raw_info[1+num_ghosts:]

        snack_map = {(sx, sy): (stype, sexists)
                     for sx, sy, stype, sexists in current_snacks_tuples}

        formatted_snacks = []
        for s in initial_snacks:
            pos = (s.x, s.y)
            if pos in snack_map:
                stype, sexists = snack_map[pos]
                formatted_snacks.append((s.x, s.y, stype, sexists))
            else:
                formatted_snacks.append((s.x, s.y, s.type, False))

        final_info = [player_info] + ghosts_info + formatted_snacks
        gui_history.append((move, final_info))

    print(f"Weighted A*: Render history ready ({len(gui_history)} frames).")
    return gui_history
