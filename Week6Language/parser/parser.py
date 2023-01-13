import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S

AP -> Adj | Adj AP | AP Adj
NP -> N | Det N | Det AP N | NP Adv | NP P NP
PP -> P NP | P S | P Det NP
VP -> V | V NP | V NP PP | VP Conj VP | V PP | Adv VP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)

    for word in words:
        # if not even a character in each word is alphabetical we remove the word.
        if not any(c.isalpha() for c in word):
            words.remove(word)
    # Lowercasing all words
    words = [words[i].lower() for i in range(len(words))]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    # By passing an argument to the tree.subtrees(filter_func) it returns an iterator
    # over all the subtrees of the tree, that pass the filter function. This lambda function
    # takes one argument t representing the current subtree being evaluated. If the current
    # subtree is labeled 'NP' and it doesn't have any children labeled 'NP', the lambda
    # function returns True and that subtree is included in the returned iterator.
    subtrees_iterator = tree.subtrees(lambda t: t.label() == 'NP' and all(child.label() != 'NP' for child in t))

    # Now we iterate through each subtree of the iterator and append it to our chunks.
    for subtree in subtrees_iterator:
         np_chunks.append(subtree)
    return np_chunks
    
    # It can also be done in one line: 
    #return [subtree for subtree in tree.subtrees(lambda t: t.label() == 'NP' and all(child.label() != 'NP' for child in t))]
    

if __name__ == "__main__":
    main()
