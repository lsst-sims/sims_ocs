from builtins import str
import collections
import inspect

__all__ = ["topic_strdict"]

def topic_strdict(topic, float_format="{:.3f}"):
    """Return a dictionary of stringified attribute values.

    This function takes a Scheduler DDS topic instance and creates a dictionary from the
    instance attributes. The attribute names are string and their associated values are also
    turned into strings.

    Parameters
    ----------
    topic : SALPY_scheduler.<topic>
        A Scheduler DDS topic instance
    float_format : str
        A format style precision limit for float values.

    Returns
    -------
    dict
        A dictionary of instance attributes (keys) and values both as strings.
    """
    output = collections.OrderedDict()
    for k, v in inspect.getmembers(topic):
        if not k.startswith("__"):
            try:
                if v.is_integer():
                    vs = str(v)
                else:
                    vs = float_format.format(v)
            except AttributeError:
                vs = str(v)
            output[k] = vs
    return output
