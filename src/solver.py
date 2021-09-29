# -*-coding: utf8-*-

class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        Ces contraintes seront appliquées en appelant la méthode ``reduce_all_domains``.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.grid = grid
        self.cases_vides_possibilites = {} # un dict avec les clés = un tuple des coordonnées (row, col) d'une case, 
                                           # et les valeurs = un set des valeurs possibles à cette case

        for case_vide in self.grid.get_empty_pos():
            self.cases_vides_possibilites[case_vide] = set(range(1, 10))

        self.reduce_all_domains()

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for case_vide_coords in list(self.cases_vides_possibilites.keys()):  # cast en list pour faire une copie et pouvoir del
            impossibles_row = set(self.grid.get_row(case_vide_coords[0]))
            impossibles_col = set(self.grid.get_col(case_vide_coords[1]))
            impossibles_reg = set(self.grid.get_region(
                case_vide_coords[0] // 3, case_vide_coords[1] // 3))

            self.cases_vides_possibilites[case_vide_coords] = self.cases_vides_possibilites[case_vide_coords].difference(impossibles_row | impossibles_col | impossibles_reg)

            if not self.cases_vides_possibilites[case_vide_coords]:
                del self.cases_vides_possibilites[case_vide_coords]

    def reduce_domains(self, last_i, last_j, last_v):
        """À COMPLÉTER
        Cette méthode devrait être appelée à chaque mise à jour de la grille,
        et élimine la dernière valeur affectée à une case
        pour toutes les autres cases concernées par cette mise à jour (même ligne, même colonne ou même région).
        :param last_i: Numéro de ligne de la dernière case modifiée, entre 0 et 8
        :param last_j: Numéro de colonne de la dernière case modifiée, entre 0 et 8
        :param last_v: Valeur affecté à la dernière case modifiée, entre 1 et 9
        :type last_i: int
        :type last_j: int
        :type last_v: int
        """
        for case_vide_coords in list(self.cases_vides_possibilites.keys()):  # cast en list pour faire une copie et pouvoir del
            if case_vide_coords[0] == last_i or case_vide_coords[1] == last_j or (case_vide_coords[0] // 3 == last_i // 3 and case_vide_coords[1] // 3 == last_j // 3):
                self.cases_vides_possibilites[case_vide_coords].discard(last_v)

                if not self.cases_vides_possibilites[case_vide_coords]:
                    del self.cases_vides_possibilites[case_vide_coords]

    def commit_one_var(self):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        for case_vide_coords, case_vide_valeurs in self.cases_vides_possibilites.items():
            if len(case_vide_valeurs) == 1:
                last = (case_vide_coords[0], case_vide_coords[1], list(case_vide_valeurs)[0])
                self.grid.write(last[0], last[1], last[2])
                return last

    def solve_step(self):
        """À COMPLÉTER
        Cette méthode alterne entre l'affectation de case pour lesquelles il n'y a plus qu'une possibilité
        et l'élimination des nouvelles valeurs impossibles pour les autres cases concernées.
        Elle répète cette alternance tant qu'il reste des cases à remplir,
        et correspond à la résolution de Sudokus dits «simple».

        *Variante avancée: en plus de vérifier s'il ne reste plus qu'une seule possibilité pour une case,
        il est aussi possible de vérifier s'il ne reste plus qu'une seule position valide pour une certaine valeur
        sur chaque ligne, chaque colonne et dans chaque région*
        """
        i = 0
        i_max = len(self.grid.get_empty_pos())
        while len(self.grid.get_empty_pos()) != 0 and i < i_max:
            i += 1
            last = self.commit_one_var()
            if last != None:
                self.reduce_domains(last[0], last[1], last[2])
                i = 0
                i_max -= 1

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        if len(self.cases_vides_possibilites) == 0:
            return False

        for possibilites in self.cases_vides_possibilites.values():
            if not possibilites:
                return False

        return True

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        return not self.grid.get_empty_pos()

    def branch(self):
        """À COMPLÉTER
        Cette méthode sélectionne une variable libre dans la solution partielle actuelle,
        et crée autant de sous-problèmes que d'affectation possible pour cette variable.
        Ces sous-problèmes seront sous la forme de nouvelles instances de solver
        initialisées avec une grille partiellement remplie.
        *Variante avancée: Renvoyez un générateur au lieu d'une liste.*
        *Variante avancée: Un choix judicieux de variable libre,
        ainsi que l'ordre dans lequel les affectations sont testées
        peut fortement améliorer les performances de votre solver.*
        :return: Une liste de sous-problèmes ayant chacun une valeur différente pour la variable choisie
        :rtype: list of SudokuSolver
        """
        instances = []
        possibilites_triees = sorted(self.cases_vides_possibilites.items(), key=lambda v: len(v[1]))  # tri par taille des set de possibilités

        # on choisit la premiere possibilites_triees, aka celle avec le moins de choix possible
        (case_coos, case_values) = possibilites_triees[0]

        for valeur in case_values:
            new_grid = self.grid.copy()
            new_grid.write(case_coos[0], case_coos[1], valeur)
            instances.append(SudokuSolver(new_grid))

        return instances

    def solve(self):
        """
        Cette méthode implémente la fonction principale de la programmation par contrainte.
        Elle cherche d'abord à affiner au mieux la solution partielle actuelle par un appel à ``solve_step``.
        Si la solution est complète, elle la retourne.
        Si elle est invalide, elle renvoie ``None`` pour indiquer un cul-de-sac dans la recherche de solution
        et déclencher un retour vers la précédente solution valide.
        Sinon, elle crée plusieurs sous-problèmes pour explorer différentes possibilités
        en appelant récursivement ``solve`` sur ces sous-problèmes.
        :return: Une solution pour la grille de Sudoku donnée à l'initialisation du solver
        (ou None si pas de solution)
        :rtype: SudokuGrid or None
        """
        self.solve_step()

        if self.is_solved():
            return self.grid

        if self.is_valid():
            instances = self.branch()
            for instance in instances:
                s = instance.solve()
                if s != None:
                    return s
