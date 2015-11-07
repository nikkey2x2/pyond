import importlib

__all__ = ['type2class', 'class2type', 'load_code']

def type2class(typename):   # /obj/laser -> Obj_Laser
    return '_'.join([x.title() for x in typename[1:].split('/')])


def class2type(typename):   # Obj_Laser -> /obj/laser
    return '/'+'/'.join([x.lower() for x in typename.split('_')])


def load_code(includes):
    defines = {}
    for fl in includes:
        inc = importlib.import_module(fl)
        for cls in inc.__all__:
            defines[cls] = getattr(inc, cls)
    return defines
