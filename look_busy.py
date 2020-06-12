#! /usr/bin/env python

import configs
import repo_writer
import util

if __name__ == '__main__':
    from sys import argv
    from random import normalvariate, choice
    from math import floor

    if len(argv) is not 4:
        print(
            f'Usage: {argv[0]} <path to config> <avg commits> <std dev commits>'
        )

    config_path = argv[1]

    with open(config_path) as f:
        config = configs.from_yaml(f)

    if config['repositories'] is None:
        raise configs.InvalidConfig()

    repo = choice(config['repositories'])

    writer = repo_writer.GitRepoWriter(repo['path'])

    reps = floor(normalvariate(int(argv[2]), int(argv[3])))
    if reps < 0:
        reps = 0

    writer.write(reps)
    writer.push()
