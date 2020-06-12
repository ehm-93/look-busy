class InvalidConfig(Exception):
    pass


def from_yaml(config_yaml):
    """Import a YAML config file.

    :return:
        a dict loaded from the YAML file
    """
    assert config_yaml

    from yaml import safe_load

    return safe_load(config_yaml)
