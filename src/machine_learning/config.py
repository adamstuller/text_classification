from os import path
config = {
    "path_to_models": path.join(path.dirname(path.realpath(__file__)), 'data', 'models'),
    "path_to_datasets": path.join(path.dirname(path.realpath(__file__)), 'data', 'datasets'),
    "classes": ['Neutral', 'Súťaž', 'Interakcia', 'Ostatné', 'Ponuka produktov',
                'Cena produktov / benefity', 'Problémy s produktom', 'Odpovede',
                'Produkt', 'Otázky', 'Pobočka']
}
