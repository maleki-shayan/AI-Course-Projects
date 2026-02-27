# File: core/solvers/astar_solver.py

from ..environment.game import PacmanGame
from .heuristics import farthest_snack_heuristic
from copy import deepcopy
import time

def astar_solver(game: PacmanGame, timeout=120):
    """
    A* Search implementation using only Python lists (no heapq).
    Based only on PacmanGame public API.
    Generates GUI-safe render history with fixed snack count.
    """
    start_time = time.time()

    initial_game = deepcopy(game)
    initial_state = initial_game.get_state()
    initial_snacks = deepcopy(initial_game.snacks)
    num_ghosts = len(initial_game.ghosts)

    g_costs = {initial_state: 0}
    h_cost_init = farthest_snack_heuristic(initial_game)
    f_cost_init = g_costs[initial_state] + h_cost_init

    open_list = [(f_cost_init, g_costs[initial_state], initial_game, [])]
    visited = set()

    found_path = None
    print("A* (simple list): Starting search...")

    while open_list:
        if time.time() - start_time > timeout:
            print("A*: Timeout reached.")
            return None

        best_index = 0
        for i in range(1, len(open_list)):
            if open_list[i][0] < open_list[best_index][0]:
                best_index = i

        f_cost, g_cost, current_game, path = open_list.pop(best_index)
        state = current_game.get_state()

        if state in visited:
            continue
        visited.add(state)

        if current_game.is_goal():
            found_path = path
            print(f"A*: Goal found! Path length = {len(found_path)}")
            break

        for next_game, action, cost in current_game.get_next_states():
            next_state = next_game.get_state()
            new_g = g_cost + cost
            new_h = farthest_snack_heuristic(next_game)
            new_f = new_g + new_h

            if next_state not in g_costs or new_g < g_costs[next_state]:
                g_costs[next_state] = new_g
                open_list.append((new_f, new_g, next_game, path + [action]))

    if found_path is None:
        print("A*: No solution found.")
        return None

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

    final_render_history = []
    for move, raw_info in raw_history:
        player_info = raw_info[0]
        ghosts_info = raw_info[1:1+num_ghosts]
        current_snacks_tuples = raw_info[1+num_ghosts:]

        snack_map = {(sx, sy): (stype, sexists)
                     for sx, sy, stype, sexists in current_snacks_tuples}

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

    print(f"A*: Render history ready ({len(final_render_history)} frames).")
    return final_render_history
