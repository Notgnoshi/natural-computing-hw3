from abc import ABCMeta as NativeABCMeta
from abc import abstractmethod


class DummyAttribute:
    pass


def abstractattribute(obj=None):
    """Enforce definition of instance attributes."""
    if obj is None:
        obj = DummyAttribute()
    obj.__is_abstractattribute__ = True
    return obj


class ABCMeta(NativeABCMeta):
    """A metaclass to enforce the definition of instance attributes.

    Source: https://stackoverflow.com/a/50381071/3704977
    """

    def __call__(cls, *args, **kwargs):
        instance = NativeABCMeta.__call__(cls, *args, **kwargs)
        abstractattributes = {
            name
            for name in dir(instance)
            if getattr(getattr(instance, name), "__is_abstractattribute__", False)
        }
        if abstractattributes:
            raise NotImplementedError(
                "Can't instantiate abstract class {} with"
                " abstract attributes: {}".format(cls.__name__, ", ".join(abstractattributes))
            )
        return instance
