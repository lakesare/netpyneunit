import sciunit

from sciunit.models import RunnableModel
from .backends.netpyne_backend import NetpyneBackend


class NetpyneModel(RunnableModel):
    def __init__(self, name=None, backend=NetpyneBackend, attrs=None):
        super().__init__(
            name, backend=backend, attrs=attrs
        )  # , backend="Netpyne", attrs=attrs)
