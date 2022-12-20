import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_destribution = dict()

    # If page has no outgoing links, we pretend it has links to all pages in
    # the corpus, including itself.We assume that the PageRank of every page
    # is 1 / N (i.e., equally likely to be on any page), N = total number
    # of pages in corpus.
    if len(corpus[page]) == 0:
        for pages in corpus:
            probability_destribution[pages] =  1 / len(corpus)
        return probability_destribution
    else:        
        #We add all pages to the prob. dest. and their probabilities.
        probability_destribution.update([(key, 0) for key in corpus])

        for pages in probability_destribution:
            # With probability 1 - damping_factor, we must divide (1 - damp.
            # fact.) by the number of pages in the corpus.
            # probability_random = (1 - damping_factor) / len(corpus)
            probability_destribution[pages] += ((1 - damping_factor) / len(corpus))

            if pages in corpus[page]:
                # With probability damping_factor, We must divide damp. fact.
                # by the number of links associated to the current page.
                # probability_damping_factor = damping_factor / len(corpus[page])
                probability_destribution[pages] += (damping_factor / len(corpus[page]))
        
    return probability_destribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimated_pagerank = dict()
    # We need to count how frequently a key appears, according to our 
    # transition model.
    counts = dict()

    # We add all pages to the estimated pagerank
    estimated_pagerank.update([(key, 0) for key in corpus])
    counts.update([(key, 0) for key in corpus])

    # The first sample is random, we copy the key to use it later, since
    # we need to check the transition model of every key. 
    first_sample = random.choice(list(estimated_pagerank.keys()))
    iterative_sample = first_sample
    counts[first_sample] += 1

    for i in range(1, n):
        # We pass the previous sample(the first sample first) into our
        # transition_model function, to get the probabilities for the next
        # sample.
        transition_models = transition_model(corpus, iterative_sample, damping_factor)

        # For every transition model of every sample we check the probability
        # of the user clicking each page and according to that probability
        # we choose the most likely and we sum one to its respective count.
        for key, value in transition_models.items():
            percentage = value 
            random_number = random.random()
            if random_number <= percentage:
                counts[key] += 1
                iterative_sample = key

    # Now we must divide these counts by the number of samples to get
    # our pagerank, and finally we copy the results to the estimated_pagerank.
    for key, value in counts.items():
        percentage = value / n 
        estimated_pagerank[key] = percentage

    return estimated_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimated_pagerank = dict()
    old_values = dict()

    # We assign each page a rank of 1 / N.
    estimated_pagerank.update([(key, 1 / len(corpus)) for key in corpus])
    old_values.update([(key, 0) for key in corpus])

    #State of the while of the loop
    var = True
    probability_random = (1 - damping_factor) / len(corpus)

    # Maximum variation of pageranks.
    value_to_check = 0.001

    # Variable to store sum part of the equation.
    sum_of_values = 0

    while var:
        for key, value in corpus.items():
            sum_of_values = 0
            # Store the old value of the PageRank for this page for later comparison.
            old_values[key] = estimated_pagerank[key]
            for v in value:
                # A page that has no links at all should be interpreted as having one
                # link for every page in the corpus (including itself).
                if len(corpus[v]) == 0:
                    sum_of_values += estimated_pagerank[key] * (1/len(corpus))
                else:
                    # Sum part of the equation. PR(i) divided by the number of links linked
                    # to that page.
                    sum_of_values += estimated_pagerank[v] / len(corpus[v])
                    
            # New pagerank for page p
            estimated_pagerank[key] = probability_random + (damping_factor * sum_of_values)

        # The control_variable makes sure that the page ranks sum to 1, otherwise
        # they can sum up to less or greater than 1.
        control_variable = sum(estimated_pagerank.values())

        for page, pagerank in estimated_pagerank.items():
            estimated_pagerank[page] = pagerank / control_variable

        # We iterate through the old values and new values and if the difference
        # between them is higher than 0.001 we continue with the while loop.
        for (k,v), (k2,v2) in zip(estimated_pagerank.items(), old_values.items()):
            if abs(estimated_pagerank[k] - old_values[k]) > value_to_check:
                var = True
                break
            else:
                var = False
                continue
    return estimated_pagerank


if __name__ == "__main__":
    main()
