curl 'http://0.0.0.0:5000/api/v1/classification/predict' \
-X POST \
-H "Content-Type:application/json" \
-d '{
"sentence": "A, B, C",
"likes": 34,
"sentiment_percentage": 12.32,
"post_id": 1233,
"posted_by_bank": 1,
"parent_class": "Neutral"
}'