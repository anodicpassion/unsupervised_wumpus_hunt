import tkinter as tk
import numpy as np
import random

states = {
    0: "Safe",
    1: "Wumpus",
    2: "Stench",
    3: "Gold",
    4: "Pit",
    5: "Breeze",
    6: "Glitter"
}


class RandomSequenceIncrement:
    def __init__(self, lower_limit: int, upper_limit: int) -> None:
        self.__guess_x = random.randint(lower_limit, upper_limit)
        self.__guess_y = random.randint(lower_limit, upper_limit)
        self.__upper_limit = upper_limit
        self.__lower_limit = lower_limit
        self.__repeat = 0

    def __call__(self) -> tuple[int, int] | bool:
        if self.__repeat > 1:
            return False
        if self.__guess_x + 1 > self.__upper_limit:
            if self.__guess_y + 1 > self.__upper_limit:
                self.__guess_y = self.__lower_limit
            else:
                self.__guess_y = self.__guess_y + 1
            self.__guess_x = self.__lower_limit
        else:
            self.__guess_x = self.__guess_x + 1
        if self.__guess_x == self.__lower_limit and self.__guess_y == self.__lower_limit:
            self.__repeat = self.__repeat + 1

        return self.__guess_x, self.__guess_y


class WumpusGUI:
    def __init__(self, grid: int = 4) -> None:
        self.__grid = grid
        self.__button_obj_array = np.zeros([self.__grid, self.__grid], dtype=tk.Button)
        self.__game_state = np.zeros(shape=[self.__grid, self.__grid, len(states)], dtype=int)
        # print(self.__game_state)
        self.__root = tk.Tk()
        self.__root.geometry("800x550")
        self.__root.title("Wumpus World")
        self.__place_controls()
        # self.__score_label = None
        self.__generate_grid()
        self.__start_game()
        self.__score = 1000
        self.__current_position = [0, 0]
        self.__game_start_flag = False
        self.__has_arrow = True
        # self.__cheat()
        self.__root.mainloop()

    def __start_game(self):
        self.__game_start_flag = False
        self.__has_arrow = True
        self.__generate_game_state()
        for i in range(self.__grid):
            for j in range(self.__grid):
                self.__button_obj_array[i, j].config(state='disabled', text="")
        self.__button_obj_array[0, 0].config(state="normal", text="Start")
        self.__score = 1000
        self.__score_label.config(text=str(self.__score))

    def move(self, pox: int, poy: int):
        # print("clicked", pox, poy)
        # self.__button_obj_array[pox, poy].config()

        if (self.__current_position != [pox, poy] or (
                self.__current_position == [0, 0] and self.__game_start_flag == False))\
                and self.__score >= 10:
            # print("taking action", pox, poy)
            self.__game_start_flag = True
            state_str = []
            if self.__game_state[pox, poy][1] == 1: state_str.append("Wumpus")
            if self.__game_state[pox, poy][2] == 1: state_str.append("Stench")
            if self.__game_state[pox, poy][3] == 1: state_str.append("Gold")
            if self.__game_state[pox, poy][4] == 1: state_str.append("Pit")
            if self.__game_state[pox, poy][5] == 1: state_str.append("Breeze")
            if self.__game_state[pox, poy][6] == 1: state_str.append("Glitter")
            if 1 not in self.__game_state[pox, poy]: state_str.append("Safe")
            self.__button_obj_array[pox, poy].config(text="\n".join(state_str))

            for i in range(self.__grid):
                for j in range(self.__grid):
                    self.__button_obj_array[i, j].config(state="disable", foreground="black")
                    if i == pox + 1 and j == poy:
                        self.__button_obj_array[i, j].config(state="normal")
                    if i == pox - 1 and j == poy:
                        self.__button_obj_array[i, j].config(state="normal")
                    if i == pox and j == poy + 1:
                        self.__button_obj_array[i, j].config(state="normal")
                    if i == pox and j == poy - 1:
                        self.__button_obj_array[i, j].config(state="normal")

            self.__score = self.__score - 10
            if self.__game_state[pox, poy][1] == 1:
                self.__score = 0
            elif self.__game_state[pox, poy][4] == 1:
                self.__score = 0
            self.__score_label.config(text=str(self.__score))
            self.__button_obj_array[pox, poy].config(state="normal", foreground="red")
            self.__current_position = [pox, poy]

        pass

    def shoot(self, direction: int):
        def kill_wumpus():
            self.__score = self.__score + 500
            self.__score_label.config(text=str(self.__score))
            print("killed")

        def missed_wumpus():
            print("missed ")
            self.__score = max([self.__score - 100, 0])
            self.__score_label.config(text=str(self.__score))

        if self.__has_arrow:
            self.__has_arrow = False
            x, y = self.__current_position[0], self.__current_position[1]
            print(direction)
            print("current location", x,y)


            if direction == 1 and self.__game_state[x-1, y][1] == 1:
                w_x, w_y = x-1, y
                print("wumpus location", w_x, w_y)
                self.__game_state[w_x, w_y][1] = 0
                state_str = []
                if self.__game_state[w_x, w_y][1] == 1: state_str.append("Wumpus")
                if self.__game_state[w_x, w_y][2] == 1: state_str.append("Stench")
                if self.__game_state[w_x, w_y][3] == 1: state_str.append("Gold")
                if self.__game_state[w_x, w_y][4] == 1: state_str.append("Pit")
                if self.__game_state[w_x, w_y][5] == 1: state_str.append("Breeze")
                if self.__game_state[w_x, w_y][6] == 1: state_str.append("Glitter")
                if 1 not in self.__game_state[w_x, w_y]: state_str.append("Safe")
                self.__button_obj_array[w_x, w_y].config(text="\n".join(state_str))

                if w_x + 1 <= self.__grid - 1:

                    self.__game_state[w_x+1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x+1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x+1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x+1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x+1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x+1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x+1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x+1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x+1, w_y].config(text="\n".join(state_str))

                if w_x - 1 >= 0:
                    self.__game_state[w_x-1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x - 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x - 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x - 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x - 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x - 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x - 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x - 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x - 1, w_y].config(text="\n".join(state_str))

                if w_y + 1 <= self.__grid - 1:
                    self.__game_state[w_x, w_y+1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y+1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y+1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y+1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y+1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y+1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y+1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y+1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y+1].config(text="\n".join(state_str))
                if w_y - 1 >= 0:
                    self.__game_state[w_x, w_y-1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y-1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y-1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y-1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y-1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y-1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y-1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y-1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y-1].config(text="\n".join(state_str))
                kill_wumpus()

            elif direction == 2 and self.__game_state[x+1, y][1] == 1:
                w_x, w_y = x+1, y
                print("wumpus location", w_x, w_y)
                self.__game_state[w_x, w_y][1] = 0
                state_str = []
                if self.__game_state[w_x, w_y][1] == 1: state_str.append("Wumpus")
                if self.__game_state[w_x, w_y][2] == 1: state_str.append("Stench")
                if self.__game_state[w_x, w_y][3] == 1: state_str.append("Gold")
                if self.__game_state[w_x, w_y][4] == 1: state_str.append("Pit")
                if self.__game_state[w_x, w_y][5] == 1: state_str.append("Breeze")
                if self.__game_state[w_x, w_y][6] == 1: state_str.append("Glitter")
                if 1 not in self.__game_state[w_x, w_y]: state_str.append("Safe")
                self.__button_obj_array[w_x, w_y].config(text="\n".join(state_str))

                if w_x + 1 <= self.__grid - 1:

                    self.__game_state[w_x + 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x + 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x + 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x + 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x + 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x + 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x + 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x + 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x + 1, w_y].config(text="\n".join(state_str))

                if w_x - 1 >= 0:
                    self.__game_state[w_x - 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x - 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x - 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x - 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x - 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x - 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x - 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x - 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x - 1, w_y].config(text="\n".join(state_str))

                if w_y + 1 <= self.__grid - 1:
                    self.__game_state[w_x, w_y + 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y + 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y + 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y + 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y + 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y + 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y + 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y + 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y + 1].config(text="\n".join(state_str))
                if w_y - 1 >= 0:
                    self.__game_state[w_x, w_y - 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y - 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y - 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y - 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y - 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y - 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y - 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y - 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y - 1].config(text="\n".join(state_str))
                kill_wumpus()

            elif direction == 3 and self.__game_state[x, y+1][1] == 1:
                w_x, w_y = x, y+1
                print("wumpus location", w_x, w_y)
                self.__game_state[w_x, w_y][1] = 0
                state_str = []
                if self.__game_state[w_x, w_y][1] == 1: state_str.append("Wumpus")
                if self.__game_state[w_x, w_y][2] == 1: state_str.append("Stench")
                if self.__game_state[w_x, w_y][3] == 1: state_str.append("Gold")
                if self.__game_state[w_x, w_y][4] == 1: state_str.append("Pit")
                if self.__game_state[w_x, w_y][5] == 1: state_str.append("Breeze")
                if self.__game_state[w_x, w_y][6] == 1: state_str.append("Glitter")
                if 1 not in self.__game_state[w_x, w_y]: state_str.append("Safe")
                self.__button_obj_array[w_x, w_y].config(text="\n".join(state_str))

                if w_x + 1 <= self.__grid - 1:

                    self.__game_state[w_x + 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x + 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x + 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x + 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x + 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x + 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x + 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x + 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x + 1, w_y].config(text="\n".join(state_str))

                if w_x - 1 >= 0:
                    self.__game_state[w_x - 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x - 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x - 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x - 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x - 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x - 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x - 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x - 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x - 1, w_y].config(text="\n".join(state_str))

                if w_y + 1 <= self.__grid - 1:
                    self.__game_state[w_x, w_y + 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y + 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y + 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y + 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y + 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y + 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y + 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y + 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y + 1].config(text="\n".join(state_str))
                if w_y - 1 >= 0:
                    self.__game_state[w_x, w_y - 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y - 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y - 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y - 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y - 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y - 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y - 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y - 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y - 1].config(text="\n".join(state_str))
                kill_wumpus()
            elif direction == 4 and self.__game_state[x, y-1][1] == 1:
                w_x, w_y = x, y-1
                print("wumpus location", w_x, w_y)
                self.__game_state[w_x, w_y][1] = 0
                state_str = []
                if self.__game_state[w_x, w_y][1] == 1: state_str.append("Wumpus")
                if self.__game_state[w_x, w_y][2] == 1: state_str.append("Stench")
                if self.__game_state[w_x, w_y][3] == 1: state_str.append("Gold")
                if self.__game_state[w_x, w_y][4] == 1: state_str.append("Pit")
                if self.__game_state[w_x, w_y][5] == 1: state_str.append("Breeze")
                if self.__game_state[w_x, w_y][6] == 1: state_str.append("Glitter")
                if 1 not in self.__game_state[w_x, w_y]: state_str.append("Safe")
                self.__button_obj_array[w_x, w_y].config(text="\n".join(state_str))

                if w_x + 1 <= self.__grid - 1:

                    self.__game_state[w_x + 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x + 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x + 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x + 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x + 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x + 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x + 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x + 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x + 1, w_y].config(text="\n".join(state_str))

                if w_x - 1 >= 0:
                    self.__game_state[w_x - 1, w_y][2] = 0
                    state_str = []
                    if self.__game_state[w_x - 1, w_y][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x - 1, w_y][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x - 1, w_y][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x - 1, w_y][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x - 1, w_y][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x - 1, w_y][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x - 1, w_y]: state_str.append("Safe")
                    self.__button_obj_array[w_x - 1, w_y].config(text="\n".join(state_str))

                if w_y + 1 <= self.__grid - 1:
                    self.__game_state[w_x, w_y + 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y + 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y + 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y + 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y + 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y + 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y + 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y + 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y + 1].config(text="\n".join(state_str))
                if w_y - 1 >= 0:
                    self.__game_state[w_x, w_y - 1][2] = 0
                    state_str = []
                    if self.__game_state[w_x, w_y - 1][1] == 1: state_str.append("Wumpus")
                    if self.__game_state[w_x, w_y - 1][2] == 1: state_str.append("Stench")
                    if self.__game_state[w_x, w_y - 1][3] == 1: state_str.append("Gold")
                    if self.__game_state[w_x, w_y - 1][4] == 1: state_str.append("Pit")
                    if self.__game_state[w_x, w_y - 1][5] == 1: state_str.append("Breeze")
                    if self.__game_state[w_x, w_y - 1][6] == 1: state_str.append("Glitter")
                    if 1 not in self.__game_state[w_x, w_y - 1]: state_str.append("Safe")
                    self.__button_obj_array[w_x, w_y - 1].config(text="\n".join(state_str))
                kill_wumpus()
            else:
                missed_wumpus()

    def grab(self):
        if self.__game_state[self.__current_position[0], self.__current_position[1]][3] == 1:
            self.__score = self.__score + 1000
            self.__score_label.config(text=str(self.__score))

    def __cheat(self):

        for i in range(self.__grid):
            for j in range(self.__grid):
                state_str = []
                if self.__game_state[i, j][1] == 1: state_str.append("Wumpus")
                if self.__game_state[i, j][2] == 1: state_str.append("Stench")
                if self.__game_state[i, j][3] == 1: state_str.append("Gold")
                if self.__game_state[i, j][4] == 1: state_str.append("Pit")
                if self.__game_state[i, j][5] == 1: state_str.append("Breeze")
                if self.__game_state[i, j][6] == 1: state_str.append("Glitter")
                if 1 not in self.__game_state[i, j]: state_str.append("Safe")
                self.__button_obj_array[i, j].config(text="\n".join(state_str))

    def __place_controls(self):
        menu_frame = tk.Frame(self.__root)
        menu_frame.pack(fill="both", pady=10)
        menu = tk.Frame(menu_frame)
        tk.Button(menu, text="Restart", command=self.__start_game).grid(row=0, column=0, sticky="W")
        tk.Button(menu, text="Cheat", command=self.__cheat).grid(row=0, column=1, sticky="W")
        menu.pack(anchor="w")

        # tk.Button(menu_frame, text="Start Game", command=self.__generate_game_state).pack(anchor="nw")
        score_frame = tk.Frame(menu_frame)
        score_frame.place(relx=0.9, y=13, anchor=tk.CENTER)
        tk.Label(score_frame, text="Score: ", font=("Calibri", 18)).grid(row=0, column=0)
        self.__score_label = tk.Label(score_frame, text="1000", font=("Calibri", 18))
        self.__score_label.grid(row=0, column=1)

    def __generate_game_state(self):
        self.__game_state = np.zeros(shape=[self.__grid, self.__grid, len(states)], dtype=int)

        # generate wumpus position
        wumpus_x, wumpus_y = 0, 0
        while wumpus_x <= 1 and wumpus_y <= 1:
            wumpus_x = random.randint(0, self.__grid - 1)
            wumpus_y = random.randint(0, self.__grid - 1)
        self.__game_state[wumpus_x, wumpus_y][1] = 1

        # generating stench
        if wumpus_x + 1 <= self.__grid - 1:
            self.__game_state[wumpus_x + 1, wumpus_y][2] = 1
        if wumpus_x - 1 >= 0:
            self.__game_state[wumpus_x - 1, wumpus_y][2] = 1
        if wumpus_y + 1 <= self.__grid - 1:
            self.__game_state[wumpus_x, wumpus_y + 1][2] = 1
        if wumpus_y - 1 >= 0:
            self.__game_state[wumpus_x, wumpus_y - 1][2] = 1

        # generating gold
        gold_x, gold_y = 0, 0
        while gold_x <= 1 and gold_y <= 1:
            gold_x, gold_y = random.randint(1, self.__grid - 1), random.randint(1, self.__grid - 1)
        self.__game_state[gold_x, gold_y][3] = 1

        # generating glitter
        if gold_x + 1 <= self.__grid - 1:
            self.__game_state[gold_x + 1, gold_y][6] = 1
        if gold_x - 1 >= 0:
            self.__game_state[gold_x - 1, gold_y][6] = 1
        if gold_y + 1 <= self.__grid - 1:
            self.__game_state[gold_x, gold_y + 1][6] = 1
        if gold_y - 1 >= 0:
            self.__game_state[gold_x, gold_y - 1][6] = 1

        # generating pits
        pits_count = 3
        pits_list = []

        def check_pits_adjacency(x, y):
            for i in pits_list:
                if (x == i[0] and y == i[1]) \
                        or (x + 1 == i[0] and y == i[1]) or (x - 1 == i[0] and y == i[1]) \
                        or (x == i[0] and y + 1 == i[1]) or (x == i[0] and y - 1 == i[1]) \
                        or (x + 1 == i[0] and y + 1 == i[1]) or (x - 1 == i[0] and y - 1 == i[1]) \
                        or (x - 1 == i[0] and y + 1 == i[1]) or (x + 1 == i[0] and y - 1 == i[1]):
                    return True  # True to regenerate co-ordinates
            else:
                return False

        def check_gold_location(x, y):
            if x == gold_x and y == gold_y:
                return True
            else:
                return False

        def check_wumpus_location(x, y):
            if x == wumpus_x and y == wumpus_y:
                return True
            else:
                return False

        def pit_safe(x, y):

            if x <= 1 and y <= 1:
                return True
            else:
                return False

        regenerate_flag = False

        for _ in range(pits_count):
            pit_guess = RandomSequenceIncrement(1, self.__grid - 1)
            pit_x, pit_y = 0, 0
            while pit_safe(pit_x, pit_y) or check_gold_location(pit_x, pit_y) \
                    or check_pits_adjacency(pit_x, pit_y) or check_wumpus_location(pit_x, pit_y):
                _temp = pit_guess()
                if _temp is False:
                    regenerate_flag = True
                    break
                else:
                    pit_x, pit_y = _temp
            if regenerate_flag:
                break
            pits_list.append([pit_x, pit_y])
            self.__game_state[pit_x, pit_y][4] = 1

            # generating breeze
            if pit_x + 1 <= self.__grid - 1:
                self.__game_state[pit_x + 1, pit_y][5] = 1
            if pit_x - 1 >= 0:
                self.__game_state[pit_x - 1, pit_y][5] = 1
            if pit_y + 1 <= self.__grid - 1:
                self.__game_state[pit_x, pit_y + 1][5] = 1
            if pit_y - 1 >= 0:
                self.__game_state[pit_x, pit_y - 1][5] = 1

        if regenerate_flag:
            print("Stuck in infinite loop...\n\tregenerating... ")
            self.__generate_game_state()

    def __move_button_config(self, button_obj, posX: int, posY: int):
        button_obj.config(command=lambda: self.move(posX, posY))
        self.__button_obj_array[posX, posY] = button_obj

    def __generate_grid(self):
        main_box_frame = tk.Frame(self.__root)
        main_box_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frame = tk.Frame(self.__root, )
        frame.pack()

        for i in range(self.__grid):
            for j in range(self.__grid):
                button = tk.Button(frame, width=6, height=5, borderwidth=0, state="normal")
                button.grid(row=i, column=j)
                self.__move_button_config(button, i, j)
                del button

        control_frame = tk.Frame(self.__root)
        # control_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        control_frame.pack(fill="both", pady=10)

        actions_controls = tk.LabelFrame(control_frame, text="Shoot")
        tk.Button(actions_controls, text=" Up ", command=(lambda: self.shoot(1))).grid(row=0, column=1)
        tk.Button(actions_controls, text="Down", command=(lambda: self.shoot(2))).grid(row=2, column=1)
        tk.Button(actions_controls, text="Grab", command=lambda:self.grab()).grid(row=1, column=1)
        tk.Button(actions_controls, text="Left", command=(lambda: self.shoot(4))).grid(row=1, column=0)
        tk.Button(actions_controls, text="Right", command=(lambda: self.shoot(3))).grid(row=1, column=2)
        actions_controls.pack()


if __name__ == "__main__":
    WumpusGUI()
