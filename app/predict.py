from joblib import load
from app.config import config
from os import path
import argparse
import pandas as pd
import sys


def predict_tag(pipeline, sentence: str, likes: int, sentiment_percentage: float, post_id: int, posted_by_bank: int, parent_class: str):
    df = pd.DataFrame.from_dict({
        'sentence': [sentence],
        'likes': [likes],
        'sentiment_percentage': [sentiment_percentage],
        'post_id': [post_id],
        'posted_by_bank': [posted_by_bank],
        'parent_class': [parent_class]
    })
    return pipeline.predict(df)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline-path", "-pp", dest="pipeline_path",
                        default=path.join(config['path_to_models'], f'pipeline-2020-03-26.joblib'))
    parser.add_argument("--sentence", "-s", dest="sentence")
    parser.add_argument("--likes", "-l", dest="likes", type=int)
    parser.add_argument("--sentiment-percentage", "-sp",
                        dest="sentiment_percentage", type=float)
    parser.add_argument("--post-id", "-pid", dest="post_id", type=int)
    parser.add_argument("--posted-by-bank", "-pbb",
                        dest="posted_by_bank", type=int, choices=[0, 1], default=0)
    parser.add_argument("--parent-class", "-pc",
                        dest="parent_class", choices=config['classes'])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    pipe = load(args.pipeline_path)
    predicted = predict_tag(pipe, args.sentence, args.likes, args.sentiment_percentage,
                            args.post_id, args.posted_by_bank, args.parent_class)
    print(predicted)
