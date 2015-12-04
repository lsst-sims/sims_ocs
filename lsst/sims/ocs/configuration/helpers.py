def load_config(config_obj, ifiles):
    """Apply override file to configuration object.

    This function does the actual work of going through the override files and applying the
    correct one to the given configuration object.

    Args:
        config_obj (pex.config.ConfigField): The configuration object to apply overrides.
        ifiles (list): The list of overriding configuration files.
    """
    for ifile in ifiles:
        try:
            config_obj.load(ifile)
        except AssertionError:
            # Not the right configuration file, so do nothing.
            pass
