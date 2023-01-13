import nltk
import sys
import os
import string
import math
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mapping = dict()

    for file_names in os.listdir(directory):
        paths_files = os.path.join(directory, file_names)
        # Without encoding it can't read certain characters in the third file.
        with open(paths_files, 'r', encoding='utf-8') as file:
            contents = file.read()
            mapping[file_names] = contents
    return mapping

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    cleaned_words = []
    for word in words:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            cleaned_words.append(word)
    return cleaned_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    documents_containing_word = dict()
    idf_values = dict()
    total_documents = len(documents.keys())

    for document in documents:
        # We convert the list into a set in order to avoid counting duplicate words.
        for word in set(documents[document]):
            if word not in documents_containing_word:
                documents_containing_word[word] = 1
            else:
                # The word appears in one more document
                documents_containing_word[word] += 1
        # Calculate IDF values for each word
        for word, count_documents in documents_containing_word.items():
            idf_values[word] = math.log((total_documents / count_documents))
    #print(idf_values)
    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames_score = {file: 0 for file in files.keys()}

    for document, words in files.items():
        # More efficient using counter than another nested for loop, counter returns
        # dictionary.
        tf = Counter(words)
        tf_idf = 0
        for word in query:
            # Words in the query that do not appear in the file should not contribute to
            # the file’s score.
            if word in tf:
                # We calculate tf-idf for each word in each document and we assign that score
                # to filenames_score.
                tf_idf = tf[word] * idfs[word]
                filenames_score[document] += tf_idf

    filenames = [k for k, v in sorted(filenames_score.items(), key=lambda item: item[1], reverse=True)]
    #print(filenames)
    return filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # First value of the list will represent matching word measure, the second, query term
    # density.
    sentences_count = {sentence: [0, 0] for sentence in sentences.keys()}

    for sentence in sentences:
        # For each word in the query we check if it also appears in the sentence's values.
        match_words = 0
        for word in query:
            if word in sentences[sentence]:
                # We calculate “matching word measure” (the sum of IDF values for any word in
                # the query that also appears in the sentence).
                sentences_count[sentence][0] += idfs[word]
                # Words in the sentence that are also words in the query.
                match_words += 1
        # Proportion of words in the sentence that are also words in the query.
        query_term_density = match_words / len(nltk.word_tokenize(sentence))
        sentences_count[sentence][1] = query_term_density

    #print(sentences_count)
    return [s for s, (mwm,qtd) in sorted(sentences_count.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)][:n]


if __name__ == "__main__":
    main()
