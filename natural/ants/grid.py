from natural.abc import ABCMeta, abstractattribute, abstractmethod


class Grid(metaclass=ABCMeta):
    @abstractattribute
    def grid_size(self):
        pass

    @abstractattribute
    def num_ants(self):
        pass

    @abstractattribute
    def radius(self):
        pass

    @abstractattribute
    def k1(self):
        pass

    @abstractattribute
    def k2(self):
        pass

    @abstractattribute
    def colors(self):
        pass


    @abstractattribute
    def ants(self):
        pass

    @abstractmethod
    def init_grid(self):
        pass

    @abstractmethod
    def init_ants(self):
        pass

    @abstractmethod
    def getkernel(self, x, y):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def plot(self, blocking=False):
        pass
