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
        return self.convert_tile_to_grid(self)

    @staticmethod
    def get_mouse_grid_coord():
        x = pygame.mouse.get_pos()[0] // Tile.block_size
        y = pygame.mouse.get_pos()[1] // Tile.block_size
        return x, y

    @staticmethod
    def convert_tile_to_grid(tile):
        x = tile.left // Tile.block_size
        y = tile.top // tile.block_size

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
    path_colour = (173, 216, 230)

    def __init__(self, left, top, width, height):
        super(TraversableTile, self).__init__(left, top, width, height)
        self.change_colour(self.default_colour)
        self.g = 0
        self.g = 0

    def distance_to(self, tile):
        this_x, this_y = Tile.convert_tile_to_grid(self)
        other_x, other_y = Tile.convert_tile_to_grid(tile)

        x_diff = abs(this_x - other_x) * 10
        y_diff = abs(this_y - other_y) * 10

        return round(math.sqrt(x_diff**2 + y_diff**2))

    def get_touching_walkways(self, board):
        touching_walkways = []
        current_x, current_y = self.get_coords()

        if Tile.is_valid_path(board, current_x, current_y, -1, -1):
            searched_tile = board.grid[current_x - 1][current_y - 1]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, -1, 0):
            searched_tile = board.grid[current_x - 1][current_y]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, -1, 1):
            searched_tile = board.grid[current_x - 1][current_y + 1]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, 0, -1):
            searched_tile = board.grid[current_x][current_y - 1]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, 0, 1):
            searched_tile = board.grid[current_x][current_y + 1]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, -1):
            searched_tile = board.grid[current_x + 1][current_y - 1]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, 0):
            searched_tile = board.grid[current_x + 1][current_y]
            touching_walkways.append(searched_tile)

        if Tile.is_valid_path(board, current_x, current_y, 1, 1):
            searched_tile = board.grid[current_x + 1][current_y + 1]
            touching_walkways.append(searched_tile)

        return touching_walkways


class WalkableTile(TraversableTile):

    default_colour = Tile.white
    searched_colour = (0, 0, 255)
    current_search_colour = (0, 255, 0)

    def __init__(self, tile):
        super(WalkableTile, self).__init__(tile.left, tile.top, tile.width, tile.height)
        self.change_colour(self.default_colour)


class TargetPosition(TraversableTile):

    default_colour = (255, 255, 0)

    def __init__(self, left, top, width, height):
        super(TargetPosition, self).__init__(left, top, width, height)
        self.change_colour(self.default_colour)
