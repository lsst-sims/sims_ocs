import importlib

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import General

__all__ = ["gen_prop_reg", "load_class"]

gen_prop_reg = pexConfig.makeRegistry('A registry for general proposals.', General)

def load_class(full_class_string):
    """Dynamically load a class from a string.

    This funtion is taken from the following blog:
    http://thomassileo.com/blog/2012/12/21/dynamically-load-python-modules-or-classes/

    Parameters
    ----------
    full_class_string : str
        A standard import like call.

    Returns
    -------
    cls
        An instance of the class.
    """
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)
