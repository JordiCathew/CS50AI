import sys
from collections import Counter
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # We go through each variable and through each list of words associated to that 
        # variable (self.domains is a dictionary).
        for var in self.domains.copy():
            for values in self.domains[var].copy():
                if len(values) != var.length:
                    self.domains[var].remove(values)
            #print(f"The var is: {var}, the words possible are: {self.domains[var]}")

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #print(f"The var is: {x}, the words possible are: {self.domains[x]}")
        #print(f"The var is: {y}, the words possible are: {self.domains[y]}")
        revised = False
        satisfies_constraint = self.crossword.overlaps[x, y] # It's not a function
        if satisfies_constraint == None:
            return revised

        # For every value in the domain of the variable x
        for value in self.domains[x].copy():
            count = 0
            # Index of the character of the first word (variable x) that overlaps
            index_x = satisfies_constraint[0]
            # Index of the character of the second word (variable y) that overlaps
            index_y = satisfies_constraint[1]
            for value2 in self.domains[y].copy():
                # If the particular characters do not overlap in the indeces, these words are
                # not the ones that overlap so we must delete that value from the domain of x.
                if value2[index_y] != value[index_x]:
                    count += 1
            if count == len(self.domains[y]):
                self.domains[x].remove(value)
                revised = True
        #print(f"The var is: {x}, the new words possible are: {self.domains[x]}")
        #self.order_domain_values(x, self.domains)
        return revised           

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        # We make a list of all the arcs in the problem, we exclude two arcs if they are 
        # the same.
        if arcs == None:
            for var1 in self.domains:
                for var2 in self.domains:
                    if var1 != var2:
                        queue.append((var1, var2))
        else:
            queue = arcs

        while len(queue) > 0:
            # We dequeue from the queue x and y.In AC-3, it is typically more efficient to
            # remove elements from the end of the list rather than the beginning, removing 
            # from the end: O(1), removing from the beginning: O(n).
            x, y = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x) - {y}:
                    queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var, values in self.domains.items():
            #print(f"The var is: {var}, the value(word) is: {values}")
            # If the assignment lacks a variable.
            if var not in assignment:
                return False
            # If a variable on the assignment lacks values
            if len(assignment[var]) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """ 
        # Checking if all values are different
        seen_values = []
        for value in assignment.values():
            if value in seen_values:
                return False
            seen_values.append(value)

        # Checking that every value is the correct length and Checking that there is no 
        # conflict between neighboring variables.
        for var, value in assignment.items():
            if len(value) != var.length:
                return False
            # Recall that a conflict is a square for which two variables disagree on what
            # character value it should take on.
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap != None:
                        # We access the words related to the variable neighbor and the 
                        # current and we look at the indeces where they overlap to check if
                        # they do.
                        current_word = assignment[var]
                        neighbor_word = assignment[neighbor]
                        if current_word[overlap[0]] != neighbor_word[overlap[1]]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # We initialize the list of values to 0 and store the values in the domain of var
        list_of_values = {}
        values_domain = self.domains[var]
        for value in values_domain:
            list_of_values[value] = 0
        
        for neighbors in self.crossword.neighbors(var):
            count = 0
            overlap = self.crossword.overlaps[var, neighbors]
            index_x = overlap[0]
            index_y = overlap[1]
            if overlap != None:
                for word in values_domain:
                    for word2 in self.domains[neighbors]:   
                        if word[index_x] != word2[index_y]:
                            list_of_values[word] += 1
        sorted_values = sorted(list_of_values.items(), key=lambda item: item[1])
        sorted_values = [key for key, value in sorted_values]
        return sorted_values
        # Returning in arbitrary order:
        #return [x for x in self.domains[var]]
              
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # We store the variables not in assignment and the number of words related to each 
        # variable.
        count = {}
        for var, set_of_values in self.domains.items():
            if var not in assignment:
                count[var] = len(set_of_values)
        
        # We put the variable or variables with the minimum number of values in its domain
        # in a separate dictionary
        min_value = min(count.values())
        result = {key: value for key, value in count.items() if value == min_value}
        
        # If there's a tie (more than one variable in result) we choose the variable with the
        # highest degree, if again a tie, we return one of the two.
        if len(result) > 1:
            highest_degree = {}
            for vars in result:
                number_neighbors = len(self.crossword.neighbors(vars))
                highest_degree[vars] = number_neighbors
            return max(highest_degree, key=highest_degree.get)
        else:
            # We return the only variable
            return next(iter(result))

    # Backtrack without inferences
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            # Removes key-value pair. Also, del works.
            assignment.pop(var)
        return None

def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
