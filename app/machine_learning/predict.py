from joblib import load
from app.config import config
from os import path
import argparse
import pandas as pd
import sys
from app.machine_learning.preprocessing import NLP4SKPreprocesser
from app.constants import BANKS, PEPCO, POSTED_BY_COLUMN_NAME, SENTENCE_COLUMN_NAME, SENTIMENT_PERCENTAGE_COLUMN_NAME, POST_ID_COLUMN_NAME, PARENT_CLASS_COLUMN_NAME, LIKES_COLUMN_NAME


nlp4sk_preprocesser = NLP4SKPreprocesser('sentence')


def predict_tag(pipeline, sentence: str, likes: int, sentiment_percentage: float, post_id: int, posted_by: int, parent_class=None, **kwargs):
    df = pd.DataFrame.from_dict({
        SENTENCE_COLUMN_NAME: [sentence],
        LIKES_COLUMN_NAME: [likes],
        SENTIMENT_PERCENTAGE_COLUMN_NAME: [sentiment_percentage],
        POST_ID_COLUMN_NAME: [post_id],
        POSTED_BY_COLUMN_NAME: [posted_by],
        PARENT_CLASS_COLUMN_NAME: [parent_class]
    })
    updated_df = nlp4sk_preprocesser.transform(df)
    return pipeline.predict(updated_df)[0]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline-path", "-pp", dest="pipeline_path",
                        default=path.join(config['path_to_models'], f'pipeline-2020-03-26.joblib'))
    parser.add_argument(f"--sentence", "-s", dest=SENTENCE_COLUMN_NAME)
    parser.add_argument("--likes", "-l", dest=LIKES_COLUMN_NAME, type=int)
    parser.add_argument("--sentiment-percentage", "-sp",
                        dest=SENTIMENT_PERCENTAGE_COLUMN_NAME, type=float)
    parser.add_argument("--post-id", "-pid", dest=POST_ID_COLUMN_NAME, type=int)
    parser.add_argument("--posted-by-bank", "-pbb",
                        dest=POSTED_BY_COLUMN_NAME, type=int, choices=[0, 1], default=0)
    parser.add_argument("--parent-class", "-pc",
                        dest=PARENT_CLASS_COLUMN_NAME, choices=config['classes'])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    pipe = load(args.pipeline_path)
    predicted = predict_tag(pipe, args.sentence, args.likes, args.sentiment_percentage,
                            args.post_id, args.posted_by, args.parent_class)
    print(predicted)
