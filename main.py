import pygame
from gui_menu import *
from tile import *
from threading import Thread


class Board:
    size = width, height = 600, 600
    black = (0, 0, 0)
    grid = []
    target_points = []

    def __init__(self):
        self.grid = self.generate_drawable_grid()
        self.drawing_mode = True

        global screen, grid
        pygame.init()
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill(self.black)
        Thread(target=gui, args=(self, ), daemon=True).start()  # get a thread to manage the Tkinter

    def generate_drawable_grid(self):

        drawable_grid = []

        for x in range(self.width // Tile.block_size):  # go through each possible position
            drawable_grid.append([])
            for y in range(self.height // Tile.block_size):
                drawable_grid[x].insert(y, DrawableTile(x * Tile.block_size, y * Tile.block_size, Tile.block_size,
                                                        Tile.block_size))  # Create a new tile

        return drawable_grid

    def find_path(self):
        self.convert_from_drawable_grid()

        current_tile = self.target_points[0]  # set the current tile to the first tile
        current_tile.f = 0
        open_list = [current_tile]
        closed_list = []

        while True:
            smallest_f = float("inf")
            current_tile = None

            for tile in open_list:
                if not isinstance(tile, TargetPosition):
                    tile.change_colour(WalkableTile.current_search_colour)
                if tile.f < smallest_f:
                    smallest_f = tile.f
                    current_tile = tile

            if current_tile == self.target_points[1]:  # If the path is at the end point
                parent = current_tile.parent
                while parent is not self.target_points[0]:  # while the backtrack is not at the start
                    if not isinstance(parent, TargetPosition):
                        parent.change_colour(TraversableTile.path_colour)
                    parent = parent.parent
                break  # end the search loop

            open_list.remove(current_tile)
            closed_list.append(current_tile)
            if not isinstance(current_tile, TargetPosition):
                current_tile.change_colour(WalkableTile.searched_colour)

            adjacent_tiles = current_tile.get_touching_walkways(self)  # get the 8 surrounding tiles

            for tile in adjacent_tiles:
                if not isinstance(tile, TraversableTile) or tile in closed_list:  # if the tile is not in the closed list and is not an obstacle
                    continue  # if it is then skip the tile

                current_path_g = tile.distance_to(self.target_points[0])
                current_path_h = tile.distance_to(self.target_points[1])
                current_path_f = current_path_g + current_path_h

                if tile not in open_list:  # if the tile is not in the open list
                    open_list.append(tile)
                    tile.parent = current_tile
                    tile.g = current_path_g
                    tile.h = current_path_h
                    tile.f = current_path_f
                else:
                    if current_path_g < tile.g:
                        tile.g = current_path_g
                        tile.h = current_path_h
                        tile.f = current_path_f

    def convert_from_drawable_grid(self,):
        self.drawing_mode = False
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                tile = self.grid[x][y]
                if isinstance(tile, DrawableTile):
                    if tile.is_obstacle:
                        self.grid[x][y] = Obstacle(tile)
                    else:
                        self.grid[x][y] = WalkableTile(tile)


def draw_grid(board):
    for x in board.grid:
        for tile in x:
            pygame.draw.rect(screen, Tile.border_colour, tile, 1)  # Draw the outside of the rectangle
            pygame.draw.rect(screen, tile.colour, tile.inner, 0)  # Draw the inside of the rectangle


def main():

    board = Board()

    while True:
        draw_grid(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit the game
                pygame.quit()
                sys.exit()
            if board.drawing_mode:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    x, y = Tile.get_mouse_grid_coord()  # convert the mouse position to the grid x and y coords
                    cell = board.grid[x][y]  # get the cell at the current point
                    if not isinstance(cell, TargetPosition):
                        if len(board.target_points) < 2:  # ensure that there are no more than two points set
                            board.grid[x][y] = TargetPosition(cell.left, cell.top, cell.width, cell.height)
                            board.target_points.append(board.grid[x][y])
                    else:
                        board.target_points.remove(board.grid[x][y])
                        board.grid[x][y] = DrawableTile(cell.left, cell.top, cell.width, cell.height)

        if board.drawing_mode:
            if pygame.mouse.get_pressed()[0] == 1 and pygame.mouse.get_pressed()[2] == 0:  # if lmb is clicked
                x, y = Tile.get_mouse_grid_coord()
                if not isinstance(board.grid[x][y], TargetPosition):
                    board.grid[x][y].set_obstacle(True)  # set the tile as an obstacle

            if pygame.mouse.get_pressed()[0] == 0 and pygame.mouse.get_pressed()[2] == 1:  # if rmb is clicked
                x, y = Tile.get_mouse_grid_coord()
                if not isinstance(board.grid[x][y], TargetPosition):
                    board.grid[x][y].set_obstacle(False)  # set the tile as an obstacle

        pygame.display.update()


if __name__ == "__main__":
    main()
