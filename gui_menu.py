from tkinter import *
from threading import Thread


def start_pressed(board, button):
    if len(board.target_points) >= 2:
        Thread(target=board.find_path,
               daemon=True).start()  #  start the path finding procedure
    else:
        print("Not enough target points")

def reset_pressed(board):
    board.reset()

    if board.generating_path:
        start_button["state"] = "disabled"
    else:
        start_button["state"] = "normal"


def gui(board):
    global start_button
    root = Tk()
    root.geometry("300x100")
    root.title("A* Pathfinding Example")

    start_button = Button(root,
                          text="START",
                          command=lambda: start_pressed(board, start_button))
    reset_button = Button(root,
                          text="RESET",
                          command=lambda: reset_pressed(board))

    start_button.pack()
    reset_button.pack()

    root.mainloop()