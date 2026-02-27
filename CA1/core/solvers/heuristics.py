
from ..environment.game import PacmanGame
import math
"""
Heuristic functions for informed search algorithms.
"""

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def farthest_snack_heuristic(game: PacmanGame):

    player_pos = game.player 
    remaining_snacks = [s for s in game.snacks if s.exists]

    if not remaining_snacks:
        return 0  

    max_dist = 0
    for snack in remaining_snacks:
        snack_pos = (snack.y, snack.x)
        dist = manhattan_distance(player_pos, snack_pos)
        if dist > max_dist:
            max_dist = dist
            
    return max_dist


def manhattan_to_nearest_snack(game: PacmanGame):

    player_pos = game.player
    remaining_snacks = [s for s in game.snacks if s.exists]

    if not remaining_snacks:
        return 0  

    min_dist = float("inf")
    for snack in remaining_snacks:
        snack_pos = (snack.y, snack.x)
        dist = manhattan_distance(player_pos, snack_pos)
        if dist < min_dist:
            min_dist = dist

    return min_dist
def straight_line_towards_goal(game: PacmanGame):

    player_pos = game.player
    remaining_snacks = [s for s in game.snacks if s.exists]

    if not remaining_snacks:
        return 0

    min_dist = float("inf")
    for snack in remaining_snacks:
        dy = player_pos[0] - snack.y
        dx = player_pos[1] - snack.x
        dist = math.sqrt(dy * dy + dx * dx)
        if dist < min_dist:
            min_dist = dist

    return min_dist