# Look Busy
This is a Python script which pushes commits to a dummy branch.

Not really sure what use this would be other than to deceive people into thinking you're working or maybe mildly annoying someone who has trusted you with access to their repository, but please don't do either of those things. That would be mean.

### Usage:
Setup a config file like this:
```yaml
repositories:
  - path: /path/to/my/repository
  - path: /path/to/another/repository
  - path: /path/to/one/more/repository
```

Then call the script like so:
```bash
python look_busy.py /path/to/my/config.yaml 3 2
```

A random repository will be selected from the config and a random number of commits normally distributed from 3 with stddev of 2 will be created and pushed to the `origin` remote.

### Dependencies: 
- [GitPython](https://gitpython.readthedocs.io/en/stable/)
