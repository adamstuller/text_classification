curl 'http://0.0.0.0:5000/api/v1/classification/predict' \
-X POST \
-H "Content-Type:application/json" \
-d '{
"sentence": "Kedy bude pepco v Martine?",
"likes": 34,
"sentiment_percentage": 0.32,
"post_id": 1233,
"posted_by": 0,
"parent_class": "Neutral",
"topic": "pepco"
}'