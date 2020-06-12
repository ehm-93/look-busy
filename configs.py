class InvalidConfig(Exception):
    pass


def from_yaml(config_yaml):
    assert config_yaml != None

    from yaml import safe_load

    return safe_load(config_yaml)
