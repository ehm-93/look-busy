#! /usr/bin/env python

if __name__ == '__main__':
    from configs import InvalidConfig, from_yaml
    from repo_writer import GitRepoWriter
    from random import normalvariate, choice
    from math import floor

    with open('./config.yaml') as f:
        config = from_yaml(f)

    if config['repositories'] is None:
        raise InvalidConfig()

    repo = choice(config['repositories'])

    writer = GitRepoWriter(repo['path'])

    reps = floor(normalvariate(3, 2))
    if reps < 0:
        reps = 0

    writer.write(reps)
    writer.push()
