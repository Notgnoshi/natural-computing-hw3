from abc import ABCMeta, abstractmethod

class Grid:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def grid_size(self):
        ...

    @property
    @abstractmethod
    def num_ants(self):
        ...

    @property
    @abstractmethod
    def radius(self):
        ...

    @property
    @abstractmethod
    def k1(self):
        ...

    @property
    @abstractmethod
    def k2(self):
        ...

    @property
    @abstractmethod
    def colors(self):
        ...

    @property
    @abstractmethod
    def grid(self):
        ...

    @property
    @abstractmethod
    def ants(self):
        ...

    @abstractmethod
    def init_grid(self):
        ...

    @abstractmethod
    def init_ants(self):
        ...

    @abstractmethod
    def getkernel(self, x, y):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def plot(self, blocking=False):
        ...