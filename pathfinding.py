# pathfinding.py
from abc import ABC, abstractmethod

class PathfindingAlgorithm(ABC):
    @abstractmethod
    def find_path(self, board, start_tile, end_tile, show_visual):
        """Abstract method to be implemented by all pathfinding algorithms."""
        pass

# pathfinding.py
from time import sleep
from tile import TraversableTile, WalkableTile, TargetPosition

class AStar(PathfindingAlgorithm):
    def find_path(self, board, start_tile, end_tile, show_visual):
        current_tile = start_tile
        current_tile.f = 0
        open_list = [current_tile]
        closed_list = []

        while True:
            smallest_f = float("inf")
            current_tile = None

            for tile in open_list:
                if not isinstance(tile, TargetPosition):
                    if show_visual:
                        tile.change_colour(WalkableTile.open_list_colour)
                if tile.f < smallest_f:
                    smallest_f = tile.f
                    current_tile = tile

            if current_tile == end_tile:  # If the path is at the end point
                parent = current_tile.parent
                while parent is not start_tile:  # while the backtrack is not at the start
                    if not isinstance(parent, TargetPosition):
                        parent.change_colour(TraversableTile.path_colour)
                    parent = parent.parent
                break  # end the search loop

            if len(open_list) == 0:
                gui_menu.pop_up_message("There is no possible path")
                break

            open_list.remove(current_tile)
            closed_list.append(current_tile)
            if not isinstance(current_tile, TargetPosition) and show_visual:
                current_tile.change_colour(WalkableTile.closed_list_colour)

            adjacent_tiles = current_tile.get_touching_walkways(board)  # get the 8 surrounding tiles

            for tile in adjacent_tiles:
                if not isinstance(tile, TraversableTile) or tile in closed_list:  # if the tile is not in the closed list and is not an obstacle
                    continue  # if it is then skip the tile

                current_path_g = current_tile.g + tile.distance_to(current_tile)
                current_path_h = tile.distance_to(end_tile)
                current_path_f = current_path_g + current_path_h

                if tile not in open_list:  # if the tile is not in the open list
                    open_list.append(tile)
                    tile.parent = current_tile
                    tile.g = current_path_g
                    tile.h = current_path_h
                    tile.f = current_path_f
                else:
                    if current_path_g < tile.g:
                        tile.parent = current_tile
                        tile.g = current_path_g
                        tile.h = current_path_h
                        tile.f = current_path_f

            if show_visual:
                sleep(0.01)
