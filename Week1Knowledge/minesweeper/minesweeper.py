import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines_in_cells = set()

        #If all the cells are mines or there is no mines.
        #If the count is 0 then it means that there is no board 
        #either, so we must return an empty set.
        if len(self.cells) == self.count and self.count != 0:
            mines_in_cells = self.cells
            return mines_in_cells
        else:
            #else, we don't know which cells have mines so we just return 
            #an empty set.
            return mines_in_cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe_cells = set()
        # We know for sure that if the count is 0, all the cells of self are
        # safe, otherwise, we can't know for sure, so we return an empty set.
        if self.count == 0:
            safe_cells = self.cells
            return safe_cells
        else:
            return safe_cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            #We need to update the count of mines
            self.count = self.count - 1 
        else:
            return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            return None

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        set_of_cells_for_sentence = set()

        safe = set()
        mine = set()

        #1)
        self.moves_made.add(cell)

        #2)
        self.mark_safe(cell)

        #3) We need to look at the cells that sorround the cell, remember that
        # cell is a tuple (i, j) where i is the row and j is the column.
        for neighbors_row in range(cell[0] - 1, cell[0] + 2):
            for neighbors_column in range(cell[1] - 1, cell[1] + 2):
                # We need to check if it's a valid cell, not a move that has been made,
                # if it's not a mine and if it's not the cell itself.
                if ((neighbors_row, neighbors_column) != cell and 
                    (neighbors_row, neighbors_column) not in self.moves_made and
                    (neighbors_row, neighbors_column) not in self.mines and 
                    0 <= neighbors_row < self.height and 0 <= neighbors_column < self.width):
                    set_of_cells_for_sentence.add((neighbors_row, neighbors_column))
                else:
                    if ((neighbors_row, neighbors_column) in self.mines):
                        count -= 1
                    else:
                        continue

        self.knowledge.append(Sentence(set_of_cells_for_sentence, count))

        #4)
        for sentence in self.knowledge:
            safe = sentence.known_safes()
            mine = sentence.known_mines()
            
            if (len(safe) != 0):
               for cell in safe.copy():
                   self.mark_safe(cell)
            if (len(mine) != 0):
               for cell in mine.copy():
                   self.mark_mine(cell)

        #5)
        for sentence in self.knowledge:
            # We check if the new sentence is a subset of one of the sentences 
            # in the knowledge base. If the count is 0 we can't deduce new sentences.
            if (Sentence(set_of_cells_for_sentence, count).cells.issubset(sentence.cells)
                and sentence.count > 0 and count > 0 and Sentence(set_of_cells_for_sentence, count) 
                != sentence):
                copy_sentence_cells = sentence.cells.copy()
                copy_sentence_count = sentence.count
                Sentence(copy_sentence_cells - Sentence(set_of_cells_for_sentence, count).cells, 
                         copy_sentence_count - count)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            #If there is a move that we know for sure it's safe and not made
            if move and move not in self.moves_made and move not in self.mines:
                move_chosen = move
                return move_chosen
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        print(f"{self.safes}")

        # Check which cells fulfill the condition,
        #  we check the conditions first for efficiency.
        for row in range(self.height):
            for column in range(self.width):
                if ((row, column) not in self.moves_made and 
                    (row, column) not in self.mines):
                    possible_moves.append((row, column))
        
        # If there are cells that fulfill the condition, choose one randomly,
        # if not, return none.
        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None


        
