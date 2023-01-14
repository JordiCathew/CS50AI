# Crossword

AI that generates crossword puzzles.

```bash
$ python generate.py data/structure1.txt data/words1.txt output.png
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
```

## Background

How might you go about generating a crossword puzzle? Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. We can model this sort of problem as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence).

## Usage

We need to specify one of the structures for our
crossword puzzle, we have different structures inside the data
directory, we can choose any of them. We also
have word lists inside the data directory, we 
need to specify one when we run it as well.

Additionally there's an optional argument at the end
for an image file, as by running python generate.py data/structure1.txt data/words1.txt output.png, to generate an image representation of the resulting crossword puzzle as well.

```bash
$ py generate.py data/structure.txt data/words.txt output.png
```