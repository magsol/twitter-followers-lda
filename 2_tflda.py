import argparse
import json
import os.path

from joblib import Parallel, delayed

from tflda.preprocess import clean

def parse_tweets(user_id, tweets):
    """
    Utility method for extracting the tweet content for a user.
    """
    document = clean(tweets)


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
