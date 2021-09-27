# -*-coding: utf8-*-
import sys
from multiprocessing import Value


class SudokuGrid:
    """Cette classe représente une grille de Sudoku.
    Toutes ces méthodes sont à compléter en vous basant sur la documentation fournie en docstring.
    """

    def __init__(self, initial_values_str):
        """À COMPLÉTER!
        Ce constructeur initialise une nouvelle instance de la classe SudokuGrid.
        Il doit effectuer la conversation de chaque caractère de la chaîne en nombre entier,
        et lever une exception (ValueError) si elle ne peut pas être interprétée comme une grille de Sudoku.
        :param initial_values_str: Une chaîne de caractères contenant **exactement 81 chiffres allant de 0 à 9**,
            où ``0`` indique une case vide
        :type initial_values_str: str
        """
        if len(initial_values_str) != 81:
            raise ValueError()

        self.grille = [[] for _ in range(0, 9)]

        for i, str_n in enumerate(initial_values_str):
            n = int(str_n)

            if 0 <= n <= 9:
                self.grille[i // 9].append(n)
            else:
                raise ValueError()

    @staticmethod
    def from_file(filename, line):
        """À COMPLÉTER!
        Cette méthode de classe (ou méthode statique) crée une nouvelle instance de grille de Sudoku
        à partir d'une ligne contenue dans un fichier.

        :param filename: Chemin d'accès vers le fichier à lire
        :param line: Numéro de la ligne à lire
        :type filename: str
        :type line: int
        :return: La grille de Sudoku correspondant à la ligne donnée dans le fichier donné
        :rtype: SudokuGrid
        """
        l = ""
        f = open(filename, "r")
        for i, fileline in enumerate(f):
            if i == line - 1:
                l = fileline[:-1]
                break

        f.close()
        return SudokuGrid(l)

    @staticmethod
    def from_stdin():
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille de Sudoku
        à partir d'une ligne lu depuis l'entrée standard (saisie utilisateur).
        *Variante avancée: Permettez aussi de «piper» une ligne décrivant un Sudoku.*
        :return: La grille de Sudoku correspondant à la ligne donnée par l'utilisateur
        :rtype: SudokuGrid
        """
        # return SudokuGrid(sys.stdin.read())
        return SudokuGrid(input())

    def __str__(self):
        """À COMPLÉTER!
        Cette méthode convertit une grille de Sudoku vers un format texte pour être affichée.
        :return: Une chaîne de caractère (sur plusieurs lignes...) représentant la grille
        :rtype: str
        """
        out = ""
        for row in self.grille:
            out += ''.join(str(e) for e in row) + '\n'

        return out

    def get_row(self, i):
        """À COMPLÉTER!
        Cette méthode extrait une ligne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param i: Numéro de la ligne à extraire, entre 0 et 8
        :type i: int
        :return: La liste des valeurs présentes à la ligne donnée
        :rtype: list of int
        """
        return self.grille[i]

    def get_col(self, j):
        """À COMPLÉTER!
        Cette méthode extrait une colonne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param j: Numéro de la colonne à extraire, entre 0 et 8
        :type j: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """
        return [self.grille[i][j] for i in range(len(self.grille))]

    def get_region(self, reg_row, reg_col):
        """À COMPLÉTER!
        Cette méthode extrait les valeurs présentes dans une région donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param reg_row: Position verticale de la région à extraire, **entre 0 et 2**
        :param reg_col: Position horizontale de la région à extraire, **entre 0 et 2**
        :type reg_row: int
        :type reg_col: int
        :return: La liste des valeurs présentes à la région donnée
        :rtype: list of int
        """
        out = []

        for i in range(3):
            out.extend(self.grille[3 * reg_row + i]
                       [3 * reg_col:3 * reg_col + 3])

        return out

    def get_empty_pos(self):
        """À COMPLÉTER!
        Cette méthode renvoit les positions des cases vides dans la grille de Sudoku,
        sous la forme de tuples ``(i,j)`` où ``i`` est le numéro de ligne et ``j`` le numéro de colonne.
        *Variante avancée: Renvoyez un générateur sur les tuples de positions ``(i,j)`` au lieu d'une liste*
        :return: La liste des positions des cases vides dans la grille
        :rtype: list of tuple of int
        """
        out = []
        for i, row in enumerate(self.grille):
            for j, n in enumerate(row):
                if n == 0:
                    out.append((i, j))

        return out

    def write(self, i, j, v, force=False):
        """À COMPLÉTER!
        Cette méthode écrit la valeur ``v`` dans la case ``(i,j)`` de la grille de Sudoku.
        *Variante avancée: Levez une exception si ``i``, ``j`` ou ``v``
        ne sont pas dans les bonnes plages de valeurs*
        *Variante avancée: Ajoutez un argument booléen optionnel ``force``
        qui empêche d'écrire sur une case non vide*
        :param i: Numéro de ligne de la case à mettre à jour, entre 0 et 8
        :param j: Numéro de colonne de la case à mettre à jour, entre 0 et 8
        :param v: Valeur à écrire dans la case ``(i,j)``, entre 1 et 9
        """
        if 0 <= i <= 8 and 0 <= j <= 8 and 0 <= v <= 9 and (self.grille[i][j] == 0 or force):
            self.grille[i][j] = v

    def copy(self):
        """À COMPLÉTER!
        Cette méthode renvoie une nouvelle instance de la classe SudokuGrid,
        qui doit être une copie **indépendante** de la grille de Sudoku.
        *Variante avancée: vous pouvez utiliser ``self.__new__(self.__class__)``
        pour court-circuiter l'appel à ``__init__`` et manuellement initialiser les attributs de la copie.*
        :return: Une copie de la grille courrante
        :rtype: SudokuGrid
        """
        initial_values_str = ""
        for row in self.grille:
            initial_values_str += ''.join(str(e) for e in row)

        return SudokuGrid(initial_values_str)
