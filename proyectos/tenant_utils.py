from contextvars import ContextVar

_current_institucion = ContextVar(
    "current_institucion",
    default=None,
)


def set_current_institucion(institucion):
    _current_institucion.set(institucion)


def get_current_institucion():
    return _current_institucion.get()