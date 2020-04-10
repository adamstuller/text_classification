from functools import reduce


def dict_to_map(dictionary, key, value):
    return \
        reduce(
            lambda acc, x: {
                **acc,
                **{
                    x[key]: x[value]
                }
            },
            dictionary,
            {}
        )
