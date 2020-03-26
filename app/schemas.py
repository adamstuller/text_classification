predict_schema = {
    'required': ['sentence', 'likes', 'sentiment_percentage', 'post_id', 'posted_by_bank', 'parent_class'],
    'properties': {
        'sentence': {'type': 'string'},
        'likes': {'type': 'integer'},
        'sentiment_percentage': {'type': 'number'},
        'post_id': {'type': 'integer'},
        'posted_by_bank': {
            'type': 'integer',
            'enum': [0, 1],
            'default': 0},
        'parent_class': {
            'type': 'string',
            'enum': ['Neutral', 'Súťaž', 'Interakcia', 'Ostatné', 'Ponuka produktov',
                     'Cena produktov / benefity', 'Problémy s produktom', 'Odpovede',
                     'Produkt', 'Otázky', 'Pobočka']
        }
    }
}

train_schema = {}