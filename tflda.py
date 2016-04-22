import argparse
import json
import os.path

# import gensim
from joblib import Parallel, delayed
import tweepy

from tflda.timelines import download_timelines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Twitter Friends LDA',
        epilog = 'lol moar tw33tz', add_help = 'How to use',
        prog = 'python tflda.py <args>')
    parser.add_argument("--api-key", required = True,
        help = "OAuth API key.")
    parser.add_argument("--api-secret", required = True,
        help = "OAuth API secret.")
    parser.add_argument("--access-key", required = True,
        help = "OAuth access key.")
    parser.add_argument("--access-secret", required = True,
        help = "OAuth access secret.")

    # Optional arguments.
    parser.add_argument("-o", "--output", default = "data",
        help = "Path to directory where intermediate data will be stored. [DEFAULT: ./data]")

    args = vars(parser.parse_args())
    outdir = os.path.join(".", args['output'])
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    auth = tweepy.OAuthHandler(args['api_key'], args['api_secret'])
    auth.set_access_token(args['access_key'], args['access_secret'])
    api = tweepy.API(auth)

    # First step: gather the list of friends.
    friends = api.friends_ids('magsol')
    out = Parallel(n_jobs = -1, verbose = 10)(
        delayed(download_timelines)(
            f, args['api_key'], args['api_secret'],
            args['access_key'], args['access_secret']) for f in friends)

    # Create the output dictionary to be json-serialized.
    final = {'{}'.format(fid): d for fid, d in out}
    fp = open(os.path.join(outdir, "data.json"), "w")
    json.dump(final, fp)
    fp.close()
