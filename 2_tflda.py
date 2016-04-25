import argparse
from collections import defaultdict
import json
import os.path

from gensim import corpora
from joblib import Parallel, delayed

from tflda.preprocess import clean

def parse_tweets(user_id, tweets):
    """
    Utility method for extracting the tweet content for a user.
    """
    document = clean(tweets)
    return [user_id, [w for w in document]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Twitter Friends LDA',
        epilog = 'lol moar tw33tz', add_help = 'How to use',
        prog = 'python 2_tflda.py <args>')
    parser.add_argument("-i", "--input", required = True,
        help = "Path to the JSON file of raw data from the previous step.")

    # Optional arguments.
    parser.add_argument("-o", "--output", default = "data",
        help = "Path to directory where intermediate data will be stored. [DEFAULT: ./data]")

    args = vars(parser.parse_args())
    outdir = os.path.join(".", args['output'])
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # Read the data from the previous step.
    fp = open(args['input'], "r")
    json_data = json.load(fp)
    fp.close()

    # Clean things up a bit.
    out = Parallel(n_jobs = -1, verbose = 10)(
        delayed(parse_tweets)(
            user_id, data['statuses'])
        for user_id, data in json_data.items())
    final = {user_id: doc for (user_id, doc) in out}
    fp = open(os.path.join(args['output'], "user_docs.json"), "w")
    json.dump(final, fp)
    fp.close()

    # Generate a global dictionary.
    frequencies = defaultdict(int)
    for doc in final.values():
        for w in doc:
            frequencies[w] += 1
    words = [[token for token in doc if frequencies[token] > 1]
        for doc in final.values()]
    dictionary = corpora.Dictionary(words)
    dictionary.save(os.path.join(args['output'], "vocabulary.dict"))

    # Generate vectors for all the documents.
    corpus = [dictionary.doc2bow(doc) for doc in final.values()]
    corpora.MmCorpus.serialize(os.path.join(args['output'], "corpus.mm"), corpus)
