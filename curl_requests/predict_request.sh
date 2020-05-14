curl 'http://0.0.0.0:5000/api/v1/topics/vub.banka/predict' \
-X POST \
-H "Content-Type:application/json" \
-d '{
    "dataset": [
        {
            "sentence": "",
            "likes": 34,
            "sentiment_percentage": 12.32,
            "post_id": 1233,
            "posted_by": 1,
            "parent_tag": "69"
        },
        {
            "sentence": "Dobry den zufalo hladam plytke taniere tohto vzoru. Zial v predajniach v Prievidzi su vypredane. Neviete mi pomoct kde sa daju este zohnat? Mal by to byt darcek. Dakujem. ",
            "posted_by": 0
        }
    ]
}'