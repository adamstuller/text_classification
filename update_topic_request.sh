curl http://0.0.0.0:5000/api/v1/topics -X PUT \
-H "Content-Type:application/json" \
-d '
{
    "dataset": [
        {
            "sentence": "Cokolada",
            "likes": 34,
            "sentiment_percentage": 0.52,
            "post_id": 51354,
            "posted_by": 1,
            "parent_tag": "Neutral",
            "tag": "Neutral"
        }
    ],
    "name": "banks",
    "mailto": "adam.syn007@gmail.com"
}
'
