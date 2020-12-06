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
S -> NP VP
NP -> N | NP VP | Det NP | Adj NP | NP PP | NP Conj NP | Adv NP | Adv VP | NP Adv
VP -> V | VP NP | VP PP
PP -> P NP
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
    # print("sentence: ", sentence)
    tokens = nltk.word_tokenize(sentence)
    # print("tokens: ", tokens)
    words = []
    for token in tokens:
        if any(c.isalpha() for c in token):
            words.append(token.lower())
    # print("words: ", words)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # TODO: using the library for a 'label' np... but some vp might contain a np
    # TODO: how do you look down the tree?
    # TODO: it's not recursive because you only have to go one step down...
    # nltk.tree documentation...
    # .label will show you the label of a node
    # .subtrees() .. this will give you the nltk.org/_modules/nltk/tree.html .. look at the code for this method
    # TODO: use the .height() == 2 to filter
    # print("tree: ", tree)
    np_chunks = []
    subtrees = tree.subtrees()
    for subtree in subtrees:
        # print("subtree: ", subtree)
        if subtree.label() == 'NP':
            contains_noun_phrase = False
            for child_node in subtree:
                # print("child_node: ", child_node)
                # print("child_node.label(): ", child_node.label())
                if child_node.label() == 'NP':
                    contains_noun_phrase = True
            if not contains_noun_phrase:
                # print("np_chunk added: ", subtree)
                np_chunks.append(subtree)
    # print("np_chunks: ", np_chunks)
    # print("np_chunks count: ", len(np_chunks))
    return np_chunks


if __name__ == "__main__":
    main()
