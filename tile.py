import pygame
import math
from abc import ABC


class Tile(pygame.Rect, ABC):  # Abstract tile class

    block_size = 20

    black = border_colour = (0, 0, 0)
    white = default_colour = (255, 255, 255)
    red = (255, 0, 0)

    def __init__(self, left, top, width, height):
        super(Tile, self).__init__(left, top, width, height)
        self.inner = pygame.Rect(left, top, width-1, height-1)  # create an inner rectangle to display the colour of the tile
        self.colour = Tile.white  # will default to a white tile

    def change_colour(self, colour):
        self.colour = colour

    def get_coords(self):
        x = self.left // self.block_size
        y = self.top // self.block_size

        return x, y

    @staticmethod
    def get_mouse_grid_coord():
        x = pygame.mouse.get_pos()[0] // Tile.block_size
        y = pygame.mouse.get_pos()[1] // Tile.block_size
        return x, y

    @staticmethod
    def is_valid_path(board, current_x, current_y, x_change, y_change):
        new_x = current_x + x_change
        new_y = current_y + y_change
        if new_x < 0 or new_x >= len(board.grid):
            return False

        if new_y < 0 or new_y >= len(board.grid):
            return False
        return True


class DrawableTile(Tile):
    border_colour = Tile.black
    default_colour = non_obstacle_colour = Tile.white
    obstacle_colour = Tile.black

    def __init__(self, left, top, width, height):
        super(DrawableTile, self).__init__(left, top, width, height)
        self.change_colour(self.default_colour)
        self.is_obstacle = False

    def set_obstacle(self, is_obstacle_state):
        self.is_obstacle = is_obstacle_state
        if self.is_obstacle:
            self.change_colour(self.obstacle_colour)
        else:
            self.change_colour(self.non_obstacle_colour)


class Obstacle(Tile):

    default_colour = Tile.black

    def __init__(self, tile):
        super(Obstacle, self).__init__(tile.left, tile.top, tile.width, tile.height)
        self.change_colour(self.default_colour)


class TraversableTile(Tile, ABC):
    path_colour = (255, 255, 0)

    def __init__(self, left, top, width, height):
        super(TraversableTile, self).__init__(left, top, width, height)
        self.change_colour(self.default_colour)
        self.g = 0
        self.g = 0

    def distance_to(self, tile):
        this_x, this_y = self.get_coords()
        other_x, other_y = tile.get_coords()

        x_diff = abs(this_x - other_x) * 10
        y_diff = abs(this_y - other_y) * 10

        return round(math.sqrt(x_diff**2 + y_diff**2))

    def get_touching_walkways(self, board):
        touching_walkways = []
        current_x, current_y = self.get_coords()

        # Straight neighbours

        if Tile.is_valid_path(board, current_x, current_y, -1, 0):
            top_tile = board.grid[current_x - 1][current_y]
            touching_walkways.append(top_tile)

        if Tile.is_valid_path(board, current_x, current_y, 0, -1):
            left_tile = board.grid[current_x][current_y - 1]
            touching_walkways.append(left_tile)

        if Tile.is_valid_path(board, current_x, current_y, 0, 1):
            right_tile = board.grid[current_x][current_y + 1]
            touching_walkways.append(right_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, 0):
            bottom_tile = board.grid[current_x + 1][current_y]
            touching_walkways.append(bottom_tile)

        # Diagonals
        
        if Tile.is_valid_path(board, current_x, current_y, -1, -1):
            if top_tile is not None and left_tile is not None and \
                    not isinstance(top_tile, Obstacle) and not isinstance(left_tile, Obstacle):  # make sure that the path cant teleport diagonally through a wall
                topl_tile = board.grid[current_x - 1][current_y - 1]
                touching_walkways.append(topl_tile)

        if Tile.is_valid_path(board, current_x, current_y, -1, 1):
            if top_tile is not None and right_tile is not None and \
                    not isinstance(top_tile, Obstacle) and not isinstance(right_tile, Obstacle):
                topr_tile = board.grid[current_x - 1][current_y + 1]
                touching_walkways.append(topr_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, -1):
            if bottom_tile is not None and left_tile is not None and \
                    not isinstance(bottom_tile, Obstacle) and not isinstance(left_tile, Obstacle):
                bottoml_tile = board.grid[current_x + 1][current_y - 1]
                touching_walkways.append(bottoml_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, 1):
            if bottom_tile is not None and right_tile is not None and \
                    not isinstance(bottom_tile, Obstacle) and not isinstance(right_tile, Obstacle):
                bottomr_tile = board.grid[current_x + 1][current_y + 1]
                touching_walkways.append(bottomr_tile)



        return touching_walkways


class WalkableTile(TraversableTile):

    default_colour = Tile.white
    open_list_colour = (255, 0, 0)
    closed_list_colour = (255, 100, 0)

    def __init__(self, tile):
        super(WalkableTile, self).__init__(tile.left, tile.top, tile.width, tile.height)
        self.change_colour(self.default_colour)


class TargetPosition(TraversableTile):

    default_colour = (255, 255, 0)

    def __init__(self, left, top, width, height):
        super(TargetPosition, self).__init__(left, top, width, height)
        self.change_colour(self.default_colour)
