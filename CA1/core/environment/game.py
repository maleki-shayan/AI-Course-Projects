from copy import deepcopy
from .ghost import Ghost
from .snack import Snack
import math
class PacmanGame:
    def __init__(self, is_wall, player, ghosts, snacks, move_direction=None):
        """
        Initializes the Pacman game state.
        
        Args:
            is_wall (list[list[bool]]): A 2D list representing the map walls.
            player (tuple[int, int]): The (row, col) coordinates of the player.
            ghosts (list[Ghost]): A list of Ghost objects.
            snacks (list[Snack]): A list of Snack objects.
            move_direction (str, optional): The direction of Pacman's last move. Defaults to None.
        """
        self.is_wall = is_wall
        self.player = player
        self.ghosts = deepcopy(ghosts)
        self.snacks = deepcopy(snacks)
        self.move_direction = move_direction

        # Correctly setting map dimensions
        self.height = len(is_wall)
        self.width = len(is_wall[0]) if self.height > 0 else 0

    """
        It returns a pair of move_direction and information for dynamic objects of the game.
        Store this information and return it in solvers. It's used on the GUI feature.
    """    
    def get_info(self):
        return (self.move_direction, [self.player] + [ghost.get_info() for ghost in self.ghosts] + [snack.get_info() for snack in self.snacks])

    """
        It returns the snack which is supposed to get eaten to on current state of the game.
    """
    def determine_goal(self):
        remaining_snacks = [s.type for s in self.snacks if s.exists]
        if len(remaining_snacks) == 0:
            return None
        return min(remaining_snacks)

    """
        Determines if (x, y) is in bounds of map or not.
    """
    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    """
        Determines if player/ghost can go to (x, y) without hitting a wall or getting out of bounds
    """
    def is_valid(self, x, y):
        return self.in_bounds(x, y) and not self.is_wall[x][y]

    """
        It determines if the game is finished or not.
    """
    def is_goal(self):
        return all(not b for b in [snack.exists for snack in self.snacks])
    
    """
        It returns a string form of the map at current state.
    """    
    def get_map(self) -> str:
        height = len(self.is_wall)
        width = len(self.is_wall[0])
        display_grid = [[' ' for _ in range(width)] for _ in range(height)]

        for x in range(height):
            for y in range(width):
                if self.is_wall[x][y]:
                    display_grid[x][y] = 'W'

        for snack in self.snacks:
            if snack.exists:
                display_grid[snack.x][snack.y] = f'{snack.type}'

        for g in self.ghosts:
            gx, gy = g.x, g.y
            display_grid[gx][gy] = f'{g.axis}'

        px, py = self.player
        display_grid[px][py] = 'P'

        map_string = "╔" + "═" * width + "╗" + "\n"
        for row in display_grid:
            map_string += "║" + "".join(row) + "║" + "\n"
        return map_string + "╚" + "═" * width + "╝" + "\n"
    

    """
        Use this method (or any defined method by yourself) to explore next possible states of the game.
    """
    # TODO


    def get_next_states(self):

        next_states = []
        moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

        ghost_future_states = {}
        for i, ghost in enumerate(self.ghosts):
            
            next_pos = ghost.get_next_position()

            if ghost.axis == 'H':
                 dist_from_center = abs(next_pos[1] - ghost.center[1])
            else: 
                 dist_from_center = abs(next_pos[0] - ghost.center[0])

            if not self.is_valid(*next_pos) or (ghost.radius is not None and dist_from_center > ghost.radius):
                final_direction = -ghost.direction
                if ghost.axis == 'H':
                    final_pos = (ghost.x, ghost.y + final_direction)
                else: 
                    final_pos = (ghost.x + final_direction, ghost.y)
            else:
                final_pos = next_pos
                final_direction = ghost.direction
            
            ghost_future_states[i] = (final_pos, final_direction)

        px, py = self.player
        for action, (p_dx, p_dy) in moves.items():
            pacman_next_pos = (px + p_dx, py + p_dy)

            if not self.is_valid(*pacman_next_pos):
                continue

            is_safe = True
            for i, ghost in enumerate(self.ghosts):
                ghost_future_pos, _ = ghost_future_states[i]
                
                if pacman_next_pos == ghost_future_pos or \
                   (pacman_next_pos == (ghost.x, ghost.y) and (px, py) == ghost_future_pos):
                    is_safe = False
                    break
            
            if not is_safe:
                continue

            next_game_instance = deepcopy(self)
            
            next_game_instance.player = pacman_next_pos
            next_game_instance.move_direction = action

            for i, ghost_obj in enumerate(next_game_instance.ghosts):
                new_pos, new_dir = ghost_future_states[i]
                ghost_obj.x, ghost_obj.y = new_pos
                ghost_obj.direction = new_dir

            new_snacks = []
            eaten_snack_pos = next_game_instance.player
            can_eat_B = not any(s.type == 'A' for s in next_game_instance.snacks)

            for snack in next_game_instance.snacks:
                is_on_snack = (snack.x, snack.y) == eaten_snack_pos
                if is_on_snack and (snack.type == 'A' or (snack.type == 'B' and can_eat_B)):
                    continue 
                new_snacks.append(snack)
            
            next_game_instance.snacks = new_snacks

            cost = 1
            next_states.append((next_game_instance, action, cost))

        return next_states

    
    """
        Use this method (or any defined method by yourself) to represent current state of the game.
    """
    # TODO
    
    
    def get_state(self):

        player_state = self.player

        ghost_states = tuple(sorted(
            [(g.x, g.y, g.axis, g.direction) for g in self.ghosts]
        ))

        snack_states = tuple(sorted(
            [s.get_info() for s in self.snacks if s.exists]
        ))
        
        return (player_state, ghost_states, snack_states)


