#! /usr/bin/env python

if __name__ == '__main__':
    from sys import argv
    from configs import InvalidConfig, from_yaml
    from repo_writer import GitRepoWriter
    from random import normalvariate, choice
    from math import floor

    if len(argv) is not 4:
        print(
            f'Usage: {argv[0]} <path to config> <avg commits> <std dev commits>'
        )

    config_path = argv[1]

    with open(config_path) as f:
        config = from_yaml(f)

    if config['repositories'] is None:
        raise InvalidConfig()

    repo = choice(config['repositories'])

    writer = GitRepoWriter(repo['path'])

    reps = floor(normalvariate(int(argv[2]), int(argv[3])))
    if reps < 0:
        reps = 0

    writer.write(reps)
    writer.push()
