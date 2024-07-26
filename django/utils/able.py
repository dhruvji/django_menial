from collections.abc import Iterable
import warnings
from django.utils.deprecation import RemovedInDjango60Warning

def make_hashable(value):
    """
    Attempt to make value hashable or raise a TypeError if it fails.

    The returned value should generate the same hash for equal values.
    """
    if isinstance(value, dict):
        return tuple(
            [
                (key, make_hashable(nested_value))
                for key, nested_value in sorted(value.items())
            ]
        )
    # Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    # to a tuple.
    try:
        hash(value)
    except TypeError:
        if isinstance(value, Iterable):
            return tuple(map(make_hashable, value))
        # Non-hashable, non-iterable.
        raise
    return value

# RemovedInDjango60Warning: Remove this entire module.

def is_iterable(x):
    """
    An implementation independent way of checking for iterables.
    
    Note: This function is deprecated and will be removed in Django 6.0.
    Use isinstance(..., collections.abc.Iterable) instead.
    """
    warnings.warn(
        "django.utils.itercompat.is_iterable() is deprecated. "
        "Use isinstance(..., collections.abc.Iterable) instead.",
        RemovedInDjango60Warning,
        stacklevel=2,
    )
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
