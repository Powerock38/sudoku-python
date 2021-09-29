#!/usr/bin/env python3

import sys
import os
from pynput import keyboard
from grid import SudokuGrid
from solver import SudokuSolver


class SudokuSolverTest:

    def __init__(self, grid):
        self.solver = SudokuSolver(grid)

        self.cursorX = 0
        self.cursorY = 0

        self.display()
        with keyboard.Listener(on_press=self.keyboard_input) as listener:
            listener.join()

    def display(self):
        os.system("clear")

        out = "  y 1 2 3   4 5 6   7 8 9\nx +-------+-------+-------+\n"

        for i, row in enumerate(self.solver.grid.grille):
            out += str(i+1) + " | "
            for j, n in enumerate(row):
                if n == 0:
                    char = "."
                else:
                    char = str(n)

                out += '\33[33m'

                if j == self.cursorX and i == self.cursorY:
                    out += '\33[47m' + char + '\33[0m' + " "
                else:
                    out += char + '\33[0m' + " "

                if j % 3 == 2:
                    out += "| "

            out += "\n"

            if i % 3 == 2:
                out += "  +-------+-------+-------+\n"

        print(out)

        r = "-"
        for case_vide_coords, case_vide_valeurs in self.solver.cases_vides_possibilites.items():
            if case_vide_coords == (self.cursorY, self.cursorX):
                r = str(case_vide_coords) + " : " + str(case_vide_valeurs)
        print(r + "\n")

    def keyboard_input(self, key):
        if key == keyboard.Key.up and self.cursorY > 0:
            self.cursorY -= 1

        elif key == keyboard.Key.down and self.cursorY < 8:
            self.cursorY += 1

        elif key == keyboard.Key.left and self.cursorX > 0:
            self.cursorX -= 1

        elif key == keyboard.Key.right and self.cursorX < 8:
            self.cursorX += 1

        elif hasattr(key, 'char') and key.char == 's':
            self.solver.solve()

        self.display()


if __name__ == "__main__":
    grid = SudokuGrid("349287501000000700000509002"
                      + "200095007001000400800720005"
                      + "100402000008000000000000376")

    test = SudokuSolverTest(grid)
