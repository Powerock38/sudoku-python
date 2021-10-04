#!/bin/python3
# -*-coding: utf8-*-

import sys
import os
from pynput import keyboard
from grid import SudokuGrid


class SudokuGame:

    def __init__(self, grid):
        self.grid = grid
        self.initialGrid = grid.copy()

        self.cursorX = 0
        self.cursorY = 0

        self.display()
        with keyboard.Listener(on_press=self.keyboard_input) as listener:
            listener.join()

    def display(self):
        os.system("clear")

        out = "  y 1 2 3   4 5 6   7 8 9\nx +-------+-------+-------+\n"

        for i, row in enumerate(self.grid.grille):
            out += str(i+1) + " | "
            for j, n in enumerate(row):
                if n == 0:
                    char = "."
                else:
                    char = str(n)

                isInitial = self.initialGrid.get_row(i)[j] == n and n != 0

                if isInitial:
                    color = '\33[33m'
                else:
                    color = '\33[37m'

                if j == self.cursorX and i == self.cursorY:
                    if not isInitial:
                        color = '\33[30m'
                    out += color + '\33[47m' + char + '\33[0m' + " "
                else:
                    out += color + char + '\33[0m' + " "

                if j % 3 == 2:
                    out += "| "

            out += "\n"

            if i % 3 == 2:
                out += "  +-------+-------+-------+\n"

        print(out)

    def keyboard_input(self, key):
        if key == keyboard.Key.up and self.cursorY > 0:
            self.cursorY -= 1

        elif key == keyboard.Key.down and self.cursorY < 8:
            self.cursorY += 1

        elif key == keyboard.Key.left and self.cursorX > 0:
            self.cursorX -= 1

        elif key == keyboard.Key.right and self.cursorX < 8:
            self.cursorX += 1

        elif self.pynput_sucks(key) != None:
            n = self.grid.get_row(self.cursorY)[self.cursorX]

            isInitial = self.initialGrid.get_row(self.cursorY)[self.cursorX] == n and n != 0

            self.grid.write(self.cursorY, self.cursorX, self.pynput_sucks(key), force=not isInitial, playmode=True)

        self.display()

        if self.is_win():
            print("C'est gagné !")
            exit()

    def is_win(self):
        ok_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for i in range(0, 9):
            row = self.grid.get_row(i)
            col = self.grid.get_col(i)
            if set(row) != ok_set or set(col) != ok_set:
                return False

        for i in range(0, 3):
            for j in range(0, 3):
                reg = self.grid.get_region(i, j)
                if set(reg) != ok_set:
                    return False

        return True

    def pynput_sucks(self, key):
        if hasattr(key, 'char') and key.char != None:
            upper_num_keys = ['à', '&', 'é', '"', "'", '(', '-', 'è', '_', 'ç']
            if '0' <= key.char <= '9':
                return int(key.char)
            elif key.char in upper_num_keys:
                return upper_num_keys.index(key.char)
        elif hasattr(key, 'vk') and key.vk != None and key.vk == 65437:
            return 5


if __name__ == "__main__":
    if len(sys.argv) == 3:
        grid = SudokuGrid.from_file(sys.argv[1], int(sys.argv[2]))
    else:
        print("Lecture de la grille par l'entrée standard")
        print("Vous pouvez aussi lire la grille depuis un fichier avec la syntaxe :", sys.argv[0], "<file> <line>")
        grid = SudokuGrid.from_stdin()

    SudokuGame(grid)
