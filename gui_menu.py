from tkinter import *
from tkinter import messagebox
from threading import Thread


def start_pressed(board, is_visual, algorithm):
    if len(board.target_points) >= 2:
        Thread(target=board.find_path, args=(algorithm.get(), is_visual.get()), daemon=True).start()  #  start the path finding procedure
    else:
        pop_up_message("You need to specify a start and end point by using your middle mouse button")


def pop_up_message(message):
    messagebox.showerror("Error", message)


def reset_pressed(board):
    board.reset()


def gui(board):
    global start_button, message_box
    root = Tk()
    root.geometry("300x150")
    root.title("Pathfinding Algorithm")

    is_visual = IntVar()
    is_visual.set(1)

    algorithm = StringVar()
    algorithm.set("A*")

    start_button = Button(root,
                          text="START",
                          command=lambda: start_pressed(board, is_visual, algorithm)).pack()
    reset_button = Button(root,
                          text="RESET",
                          command=lambda: reset_pressed(board)).pack()
    visual_checkbox = Checkbutton(root, text="Show Visual Search", variable=is_visual).pack()

    Label(root, text="Choose Algorithm:").pack()
    Radiobutton(root, text="A*", variable=algorithm, value="A*").pack()
    Radiobutton(root, text="Dijkstra", variable=algorithm, value="Dijkstra").pack()

    root.mainloop()
