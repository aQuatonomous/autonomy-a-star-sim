from tkinter import *
from tkinter import messagebox
from threading import Thread


def start_pressed(board, is_visual):
    if len(board.target_points) >= 2:
        Thread(target=board.find_path, args=(is_visual.get(), ), daemon=True).start()  #  start the path finding procedure
    else:
        pop_up_message("You need to specify a start and end point by using your middle mouse button")


def pop_up_message(message):
    messagebox.showinfo("Error", message)


def reset_pressed(board):
    board.reset()


def gui(board):
    global start_button, message_box
    root = Tk()
    root.geometry("300x100")
    root.title("A* Pathfinding Example")

    is_visual = IntVar()

    start_button = Button(root,
                          text="START",
                          command=lambda: start_pressed(board, is_visual)).pack()
    reset_button = Button(root,
                          text="RESET",
                          command=lambda: reset_pressed(board)).pack()
    visual_checkbox = Checkbutton(root, text="Show Visual Search", variable=is_visual).pack()

    root.mainloop()