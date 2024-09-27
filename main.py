import gui_menu
import sys
from tile import *
from threading import Thread
from time import sleep

class Board:
    size = width, height = 600, 600
    black = (0, 0, 0)
    grid = []
    target_points = []

    def __init__(self):
        self.grid = self.generate_drawable_grid()
        self.drawing_mode = True
        self.generating_path = False

        global screen, grid
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        screen.fill(self.black)
        Thread(target=gui_menu.gui, args=(self, ), daemon=True).start()  # get a thread to manage the Tkinter

    def reset(self):
        self.grid = self.generate_drawable_grid()
        self.drawing_mode = True
        self.generating_path = False
        self.target_points = []

    def generate_drawable_grid(self):

        drawable_grid = []

        for x in range(self.width // Tile.block_size):  # go through each possible position
            drawable_grid.append([])
            for y in range(self.height // Tile.block_size):
                drawable_grid[x].insert(y, DrawableTile(x * Tile.block_size, y * Tile.block_size, Tile.block_size,
                                                        Tile.block_size))  # Create a new tile

        return drawable_grid

    def find_a_star_path(self, show_visual):
        self.convert_from_drawable_grid()
        self.generating_path = True
        current_tile = self.target_points[0]  # set the current tile to the first tile
        open_list = [current_tile]
        closed_list = []

        while self.generating_path:
            smallest_f = float("inf")
            current_tile = None

            # Get the tile with the smallest `f` value
            for tile in open_list:
                if not isinstance(tile, TargetPosition):
                    if show_visual:
                        tile.change_colour(WalkableTile.open_list_colour)
                if tile.f < smallest_f:
                    smallest_f = tile.f
                    current_tile = tile

            if current_tile == self.target_points[1]:  # If the path is at the end point
                parent = current_tile.parent
                while parent is not self.target_points[0]:  # while the backtrack is not at the start
                    if not isinstance(parent, TargetPosition):
                        parent.change_colour(TraversableTile.path_colour)
                    parent = parent.parent
                self.generating_path = False
                break  # end the search loop

            if len(open_list) == 0:
                gui_menu.pop_up_message("There is no possible path")
                break

            open_list.remove(current_tile)
            closed_list.append(current_tile)
            if not isinstance(current_tile, TargetPosition) and show_visual:
                current_tile.change_colour(WalkableTile.closed_list_colour)

            adjacent_tiles = current_tile.get_touching_walkways(self)  # get the 8 surrounding tiles

            for tile in adjacent_tiles:
                if not isinstance(tile, TraversableTile) or tile in closed_list:  # if the tile is not in the closed list and is not an obstacle
                    continue  # if it is then skip the tile

                current_path_g = current_tile.g + tile.distance_to(current_tile)
                current_path_h = tile.distance_to(self.target_points[1])
                current_path_f = current_path_g + current_path_h

                if tile not in open_list:  # if the tile is not in the open list
                    open_list.append(tile)
                    tile.parent = current_tile
                    tile.g = current_path_g
                    tile.h = current_path_h
                    tile.f = current_path_f
                else:
                    if current_path_f < tile.f:
                        tile.parent = current_tile
                        tile.g = current_path_g
                        tile.h = current_path_h
                        tile.f = current_path_f

            if show_visual:
                sleep(0.01)

    def find_dijkstra_path(self, show_visual):
        self.convert_from_drawable_grid()
        self.generating_path = True
        current_tile = self.target_points[0]  # set the current tile to the first tile
        current_tile.g = 0
        open_list = [current_tile]
        closed_list = []

        while self.generating_path:
            smallest_g = float("inf")
            current_tile = None

            # Get the tile with the smallest `g` value
            for tile in open_list:
                if not isinstance(tile, TargetPosition):
                    if show_visual:
                        tile.change_colour(WalkableTile.open_list_colour)
                if tile.g < smallest_g:
                    smallest_g = tile.g
                    current_tile = tile

            if current_tile == self.target_points[1]:  # If the path is at the end point
                parent = current_tile.parent
                while parent is not self.target_points[0]:  # while the backtrack is not at the start
                    if not isinstance(parent, TargetPosition):
                        parent.change_colour(TraversableTile.path_colour)
                    parent = parent.parent
                self.generating_path = False
                break  # end the search loop

            if len(open_list) == 0:
                gui_menu.pop_up_message("There is no possible path")
                break

            open_list.remove(current_tile)
            closed_list.append(current_tile)
            if not isinstance(current_tile, TargetPosition) and show_visual:
                current_tile.change_colour(WalkableTile.closed_list_colour)

            adjacent_tiles = current_tile.get_touching_walkways(self)  # get the 8 surrounding tiles

            for tile in adjacent_tiles:
                if not isinstance(tile, TraversableTile) or tile in closed_list:  # if the tile is not in the closed list and is not an obstacle
                    continue  # if it is then skip the tile

                current_path_g = current_tile.g + tile.distance_to(current_tile)

                if tile not in open_list:  # if the tile is not in the open list
                    open_list.append(tile)
                    tile.parent = current_tile
                    tile.g = current_path_g
                else:
                    if current_path_g < tile.g:
                        tile.parent = current_tile
                        tile.g = current_path_g

            if show_visual:
                sleep(0.01)

    def find_path(self, algorithm, show_visual):
        if algorithm == "A*":
            self.find_a_star_path(show_visual)
        elif algorithm == "Dijkstra":
            self.find_dijkstra_path(show_visual)

    def convert_from_drawable_grid(self):
        grid_copy = []
        for column in self.grid:
            grid_copy.append([])
            for tile in column:
                if isinstance(tile, DrawableTile):
                    if tile.is_obstacle:
                        grid_copy[-1].append(Obstacle(tile))
                    else:
                        grid_copy[-1].append(WalkableTile(tile))

                else:
                    grid_copy[-1].append(tile)

        for target in self.target_points:
            x, y = target.get_coords()
            grid_copy[x][y] = target

        self.grid = grid_copy


def main():
    board = Board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if pygame.mouse.get_pressed()[0] and board.drawing_mode:  # if the left mouse button is pressed down
                x, y = Tile.get_mouse_grid_coord()
                board.grid[x][y].set_obstacle(True)  # set the pressed down location to an obstacle

            if pygame.mouse.get_pressed()[2] and board.drawing_mode:  # if the right mouse button is pressed down
                x, y = Tile.get_mouse_grid_coord()
                board.grid[x][y].set_obstacle(False)  # set the pressed down location to a walkable tile

            if pygame.mouse.get_pressed()[1] and board.drawing_mode:  # if the middle mouse button is pressed down
                x, y = Tile.get_mouse_grid_coord()
                if isinstance(board.grid[x][y], DrawableTile):
                    target_tile = TargetPosition(board.grid[x][y].left, board.grid[x][y].top, board.grid[x][y].width, board.grid[x][y].height)
                    board.grid[x][y] = target_tile
                    board.target_points.append(target_tile)

                if len(board.target_points) == 2:
                    board.drawing_mode = False

        for column in board.grid:  # display all the tiles
            for tile in column:
                pygame.draw.rect(screen, tile.border_colour, tile)
                pygame.draw.rect(screen, tile.colour, tile.inner)

        pygame.display.flip()


if __name__ == "__main__":
    main()
