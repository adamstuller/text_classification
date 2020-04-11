curl 'http://localhost:5000/api/v1/topics/banks/predict' \
-X POST \
-H "Content-Type:application/json" \
-d '{
    "dataset": [
        {
            "sentence": "A, B, C",
            "likes": 34,
            "sentiment_percentage": 12.32,
            "post_id": 1233,
            "posted_by": 1,
            "parent_tag": "Neutral"
        },
        {
            "sentence": "Databaza",
            "posted_by": 0
        }
    ]
}'