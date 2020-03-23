from joblib import load
from config import config
from os import path
import argparse
import pandas as pd
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--pipeline-path", "-pp", dest="pipeline_path",
                    default=path.join(config['path_to_models'], f'pipeline-2020-03-05.joblib'))
parser.add_argument("--sentence", "-s", dest="sentence")
parser.add_argument("--likes", "-l", dest="likes", type=int)
parser.add_argument("--sentiment-percentage", "-sp",
                    dest="sentiment_percentage", type=float)
parser.add_argument("--post-id", "-pid", dest="post_id", type=int)
parser.add_argument("--posted-by-bank", "-pbb",
                    dest="posted_by_bank", type=int, choices=[0, 1], default=0)
parser.add_argument("--parent-class", "-pc",
                    dest="parent_class", choices=config['classes'])


args = parser.parse_args()

if __name__ == "__main__":
    pipe = load(args.pipeline_path)
    requested_data = {
        'sentence': [args.sentence],
        'likes': [args.likes],
        'sentiment_percentage': [args.sentiment_percentage],
        'post_id': [args.post_id],
        'posted_by_bank': [args.posted_by_bank],
        'parent_class': [args.parent_class]
    }
    df = pd.DataFrame.from_dict(requested_data)
    print(pipe.predict(df))
    sys.stdout.flush()