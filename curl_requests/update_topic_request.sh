curl http://0.0.0.0:5000/api/v1/topics -X PATCH \
-H "Content-Type:application/json" \
-d '
{
    "dataset": [
        {
            "sentence": "pici boha ",
            "likes": 34,
            "sentiment_percentage": 0.52,
            "post_id": 51354,
            "posted_by": 1,
            "parent_tag": "Neutral",
            "tag": "Neutral"
        },
        {
            "sentence": "pici boha ",
            "likes": 34,
            "sentiment_percentage": 0.52,
            "post_id": 51354,
            "posted_by": 1,
            "parent_tag": "Neutral",
            "tag": "Neutral"
        },
        {
            "sentence": "pici ",
            "likes": 34,
            "sentiment_percentage": 0.52,
            "post_id": 51354,
            "posted_by": 1,
            "parent_tag": "Neutral",
            "tag": "Neutral"
        },
        {
            "sentence": "Cokolada a klada a este kadeco insie sss",
            "likes": 34,
            "sentiment_percentage": 0.52,
            "post_id": 51354,
            "posted_by": 1,
            "parent_tag": "Neutral",
            "tag": "Neutral"
        }
    ],
    "name": "banks"
}
'
