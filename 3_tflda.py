import argparse
import json
import os.path

from gensim import corpora, models

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Twitter Friends LDA',
        epilog = 'lol moar tw33tz', add_help = 'How to use',
        prog = 'python 3_tflda.py <args>')
    parser.add_argument("-i", "--input", required = True,
        help = "Path to the directory of gensim data from the previous step.")

    # Optional arguments.
    parser.add_argument("-k", "--topics", type = int, default = 10,
        help = "Number of topics to infer from the data. [DEFAULT: 10]")
    parser.add_argument("-a", "--alpha", type = float, default = 0.001,
        help = "Number of topics a single document will have. [DEFAULT: 0.001]")
    parser.add_argument("-e", "--eta", type = float, default = None,
        help = "Number of topics a word belongs to. [DEFAULT: 1/k]")
    parser.add_argument("-o", "--output", default = "data",
        help = "Path to directory where intermediate data will be stored. [DEFAULT: ./data]")

    args = vars(parser.parse_args())
    outdir = os.path.join(".", args['output'])
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # Read the data from the previous step.
    corpus = corpora.MmCorpus(os.path.join(args['input'], 'corpus.mm'))
    vocab = corpora.Dictionary.load(os.path.join(args['input'], 'vocabulary.dict'))

    # Set up the LDA.
    lda_params = {'num_topics': args['topics'],
        'passes': 100,
        'alpha': args['alpha'],
        'eta': args['eta']}
    lda = models.LdaModel(corpus, id2word = vocab, **lda_params)

    # Print out the results.
    lda.print_topics()
    lda.save(os.path.join(args['output'], "ldamodel_{}.lda".format(args['topics'])))
